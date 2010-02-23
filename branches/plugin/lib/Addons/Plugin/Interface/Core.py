import thread, time, sys, socket, re
from lib.Depend.gtk2 import gtk
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Exceptions import *
from reference import Reference
from meta import Meta

class CCore(object):
    
    def __init__(self, manager, pluginAdapter):
        self.manager = manager
        self.pluginAdapter = pluginAdapter
        self.guimanager = manager.GetGuiManager()
    
    def Error(self, addr):
        pass
    
    def Stopped(self, id):
        return True
    
    def Command(self, command, params, data, addr):
        #print 'Command', command, params, data
        
        if command['version'] == VERSION:
            try:
                com = command['command'].lower()
                callid = params.pop('__id__', None)
                if com == 'gui':
                    self._gui(command['type'], params, addr, callid)
                
                #~ elif com == 'metamodel':
                    #~ self._metamodel(command['type'], params, addr, callid)
                
                elif com == 'exec':
                    self._exec(command['type'], params, addr, callid)
                
                elif com == 'transaction':
                    self._transaction(command['type'], params, addr, callid)
                
                elif com == 'plugin':
                    self._plugin(command['type'], params, addr, callid)
                    
                else:
                    self.manager.Send(addr, RESP_UNKONWN_COMMAND, command = com, __id__ = callid)
            
            except TransactionModeUnspecifiedError:
                self.manager.Send(addr, RESP_TRANSACTION_MODE_UNSPECIFIED, __id__ = callid)
            
            except TransactionPendingError:
                self.manager.Send(addr, RESP_TRANSACTION_PENDING, __id__ = callid)
                
            except OutOfTransactionError:
                self.manager.Send(addr, RESP_OUT_OF_TRANSACTION, __id__ = callid)
            
            except (ParamValueError, ), e:
                self.manager.Send(addr, RESP_INVALID_PARAMETER, params = [i for i in e], __id__ = callid)
            
            except (ParamMissingError, ), e:
                self.manager.Send(addr, RESP_MISSING_PARAMETER, param = e[0], __id__ = callid)
                
            except (UMLException, ), e:
                self.manager.Send(addr, RESP_UNHANDELED_EXCEPTION, params = [i for i in e], __id__ = callid)
        
        else:
            self.manager.Send(addr, RESP_UNSUPPORTED_VERSION, version = command['version'], __id__ = callid)
    
    def _transaction(self, com, params, addr, callid):
        if com == 'autocommit':
            self.manager.GetTransaction(addr).StartAutocommit()
        
        elif com == 'begin':
            self.manager.GetTransaction(addr).BeginTransaction()
        
        elif com == 'commit':
            self.manager.GetTransaction(addr).CommitTransaction()
        
        elif com == 'rollback':
            self.manager.GetTransaction(addr).RollbackTransaction()
        
        else:
            self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'transaction', type = com, __id__ = callid)
        
        self.manager.Send(addr, RESP_OK, __id__ = callid)
        
    
    def _exec(self, com, params, addr, callid):
        try:
            match = re.match(r'(?P<id>([a-zA-Z_][a-zA-Z0-9_]*|#[0-9]+)).(?P<fname>\w+)$', com)
            if match is None:
                self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'exec', type = com, __id__ = callid)
                return
            identifier = match.groupdict()['id']
            fname = match.groupdict()['fname']
            
            obj = t_object(identifier)
            
            if obj is None:
                self.manager.Send(addr, RESP_INVALID_OBJECT, id = identifier, __id__ = callid)
                return
            
            if Meta.IsDestructive(obj, fname):
                result = None
                self.manager.GetTransaction(addr).Action(Meta.Execute, (obj, fname, params))
            else:
                result = Meta.Execute(obj, fname, params)
            
            self.manager.Send(addr, RESP_RESULT, __id__ = callid, result = result)
        
        except (UnknowMethodError, ), e:
            self.manager.Send(addr, RESP_UNKNOWN_METHOD, id = identifier, fname = fname, __id__ = callid)
        
        except (PluginInvalidMethodParameters, ), e:
            self.manager.Send(addr, RESP_INVALID_METHOD_PARAMETER, id = identifier, fname = fname, __id__ = callid)
            
        #~ except (TypeError, ), e:
            #~ raise ParamMissingError()
        
        #~ except (ValueError, ), e:
            #~ raise ParamValueError()
    
    def _metamodel(self, com, params, addr, callid):
        try:
            item, detail = com.split('.', 1)
            assert (detail in ('list', 'detail') and 
                item in ('metamodel', 'element', 'diagram', 'connection', 'domain'))
            
            if self.pluginAdapter.GetProject() is not None:
                metamodel = self.pluginAdapter.GetProject().GetMetamodel()
            else:
                self.manager.Send(addr, RESP_PROJECT_NOT_LOADED, __id__ = callid)
                return
            
            
            if detail == 'list':
                assert item != 'metamodel'
                if item == 'diagram':
                    result = list(metamodel.GetDiagrams())
                elif item == 'element':
                    result = [e.GetId() for e in metamodel.GetElementFactory().IterTypes()]
                elif item == 'connection':
                    result = [c.GetId() for c in metamodel.GetConnectionFactory().IterTypes()]
                elif item == 'domain':
                    result = [d.GetName() for d in metamodel.GetDomainFactory().IterTypes()]
                self.manager.Send(addr, RESP_METAMODEL_DESCRIPTION, type = com, result = result, __id__ = callid)
            
            if detail == 'detail':
                if item == 'metamodel':
                    result = {'uri': metamodel.GetUri(), 'version': metamodel.GetVersion()}
                    name = 'metamodel'
                else:
                    if 'name' in params:
                        name = params['name']
                    else:
                        raise ParamMissingError('name')
                    if item == 'diagram':
                        diagram = metamodel.GetDiagramFactory().GetDiagram(name)
                        result = {'connection': list(diagram.GetConnections()),
                                  'element': list( diagram.GetElements())}
                    if item == 'element':
                        element = metamodel.GetElementFactory().GetElement(name)
                        result = {'connection': list(element.GetConnections()),
                                  'domain':     element.GetDomain().GetName(),
                                  'identity':   element.GetIdentity(),
                                  'options':    element.GetOptions(),
                                  'resizable':  element.GetResizable()}
                    if item == 'connection':
                        connection = metamodel.GetConnectionFactory().GetConnection(name)
                        result = {'domain':   connection.GetDomain().GetName(),
                                  'identity': connection.GetConnectionIdentity()}
                    if item == 'domain':
                        domain = metamodel.GetDomainFactory().GetDomain(name)
                        result = {'attributes': [dict(id = attr, **domain.GetAttribute(attr)) for attr in domain.IterAttributeIDs()],
                                  'parsers':  list(domain.IterParsers()),}
                self.manager.Send(addr, RESP_METAMODEL_DESCRIPTION, type = com, result = result, name = name, __id__ = callid)
        
        except (AssertionError, ValueError), e:
            self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'metamodel', type = com, __id__ = callid)
        
        except (FactoryError, ), e:
            raise ParamValueError('name')
    
    def _gui(self, ctype, params, addr, callid):
        try:
            if ctype == 'add':
                mtype = params.pop('type')
                path = params.pop('path')
                if mtype in ('submenu', ):
                    name = params.pop('name', None)
                else:
                    name = params.pop('name')
                self.guimanager.AddItem(mtype, path, name, self._guiactivated, addr, **params)
                self.manager.Send(addr, RESP_GUI_ADDED, type = mtype, fullname = path + '/' + (name or ''), __id__ = callid)
            
            elif ctype == 'sensitive':
                self.guimanager.SetSensitive(params['path'], True)
                self.manager.Send(addr, RESP_GUI_SENSITIVE, path = params['path'], __id__ = callid)
            
            elif ctype == 'insensitive':
                self.guimanager.SetSensitive(params['path'], False)
                self.manager.Send(addr, RESP_GUI_INSENSITIVE, path = params['path'], __id__ = callid)
            
            elif ctype == 'warning':
                self.pluginAdapter.plugin_display_warning(params['text'])
                self.manager.Send(addr, RESP_OK, __id__ = callid)
                
            else:
                self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'gui', type = ctype, __id__ = callid)
        except (KeyError, ), e:
            raise ParamMissingError(e.message)
        
    def _guiactivated(self, item, path, addr):
        self.manager.Send(addr, RESP_GUI_ACTIVATED, path = path)
    
    def _plugin(self, ctype, params, addr, callid):
        if ctype == 'init':
            self.manager.ConnectPlugin(params['uri'], addr)
            self.manager.Send(addr, RESP_OK, __id__ = callid)
        else:
            self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'plugin', type = ctype, __id__ = callid)
            
