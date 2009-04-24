import thread, time, sys, socket, re
from interface import interface
from lib.Depend.gtk2 import gtk
from Communication.ComSpec import *
from lib.Exceptions import *
from Interface import Reference, Meta

class CProxy(object):
    
    def __init__(self, manager, app):
        self.manager = manager
        self.app = app
        self.guimanager = manager.GetGuiManager()
    
    def Error(self, addr):
        print 'ERROR', addr
    
    def Stopped(self, id):
        print 'Stopped', id
        return True
    
    def Command(self, command, params, data, addr):
        print 'Command', command, params, data
        
        if command['version'] == '1.0':
            try:
                com = command['command'].lower()
                
                if com == 'gui':
                    self._gui(command['type'].lower(), params, addr)
                
                elif com == 'metamodel':
                    self._metamodel(command['type'].lower(), params, addr)
                
                elif com == 'exec':
                    self._exec(command['type'], params, addr)
                    
                else:
                    self.manager.Send(addr, RESP_UNKONWN_COMMAND, command = com)
            
            except (ParamValueError, ), e:
                self.manager.Send(addr, RESP_INVALID_PARAMETER, params = [i for i in e])
            except (ParamMissingError, ), e:
                self.manager.Send(addr, RESP_MISSING_PARAMETER, param = e[0])
        
        else:
            self.manager.Send(addr, RESP_UNSUPPORTED_VERSION, version = command['version'])
    
    def _exec(self, com, params, addr):
        #~ try:
            match = re.match(r'(?P<id>([a-zA-Z_][a-zA-Z0-9_]*|#[0-9]+)).(?P<fname>\w+)$', com)
            if match is None:
                self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'exec', type = com)
                return
            identifier = match.groupdict()['id']
            fname = match.groupdict()['fname']
            callid = params.pop('__id__', None)
            
            if identifier.startswith('#'):
                obj = t_object(identifier)
            elif identifier == 'project':
                obj = self.app.GetProject()
            
            if obj is None:
                self.manager.Send(addr, RESP_INVALID_OBJECT, id = identifier)
                return
            
            desc = Meta.GetMethod(obj.__class__, fname)
            if desc is None:
                self.manager.Send(addr, RESP_UNKNOWN_METHOD, id = identifier, fname = fname)
                return
            else:
                params[desc[0].func_code.co_varnames[0]] = obj
            
            params = dict((key, desc[1]['params'].get(key, lambda x: x)(params[key])) for key in params)
            result = desc[0](**params)
            
            if callid is not None:
                self.manager.Send(addr, RESP_RESULT, __id__ = callid, result = desc[1]['result'](result))
            
        #~ except (TypeError, ), e:
            #~ raise ParamMissingError()
        
        #~ except (ValueError, ), e:
            #~ raise ParamValueError()
    
    def _metamodel(self, com, params, addr):
        try:
            ctype = com.split('.', 1)
            assert (len(ctype) == 2 and ctype[0] in ('list', 'detail') and 
                ctype[1] in ('metamodel', 'element', 'diagram', 'connection', 'domain'))
            
            if self.app.GetProject() is not None:
                metamodel = self.app.GetProject().GetMetamodel()
            else:
                self.manager.Send(addr, RESP_PROJECT_NOT_LOADED)
                return
            
            
            if ctype[0] == 'list':
                assert ctype[1] != 'metamodel'
                if ctype[1] == 'diagram':
                    result = list(metamodel.GetDiagrams())
                elif ctype[1] == 'element':
                    result = [e.GetId() for e in metamodel.GetElementFactory().IterTypes()]
                elif ctype[1] == 'connection':
                    result = [c.GetId() for c in metamodel.GetConnectionFactory().IterTypes()]
                elif ctype[1] == 'domain':
                    result = [d.GetName() for d in metamodel.GetDomainFactory().IterTypes()]
                self.manager.Send(addr, RESP_METAMODEL_DESCRIPTION, type = com, result = result)
            
            if ctype[0] == 'detail':
                if ctype[1] == 'metamodel':
                    result = {'uri': metamodel.GetUri(), 'version': metamodel.GetVersion()}
                    name = 'metamodel'
                else:
                    if 'name' in params:
                        name = params['name']
                    else:
                        raise ParamMissingError('name')
                    if ctype[1] == 'diagram':
                        diagram = metamodel.GetDiagramFactory().GetDiagram(name)
                        result = {'connection': list(diagram.GetConnections()),
                                  'element': list( diagram.GetElements())}
                    if ctype[1] == 'element':
                        element = metamodel.GetElementFactory().GetElement(name)
                        result = {'connection': list(element.GetConnections()),
                                  'domain':     element.GetDomain().GetName(),
                                  'identity':   element.GetIdentity(),
                                  'options':    element.GetOptions(),
                                  'resizable':  element.GetResizable()}
                    if ctype[1] == 'connection':
                        connection = metamodel.GetConnectionFactory().GetConnection(name)
                        result = {'domain':   connection.GetDomain().GetName(),
                                  'identity': connection.GetConnectionIdentity()}
                    if ctype[1] == 'domain':
                        domain = metamodel.GetDomainFactory().GetDomain(name)
                        result = {'attributes': [dict(id = attr, **domain.GetAttribute(attr)) for attr in domain.IterAttributeIDs()],
                                  'parsers':  list(domain.IterParsers()),}
                self.manager.Send(addr, RESP_METAMODEL_DESCRIPTION, type = com, result = result, name = name)
        
        except (AssertionError, ), e:
            self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'metamodel', type = com)
        
        except (FactoryError, ), e:
            raise ParamValueError('name')
    
    def _gui(self, ctype, params, addr):
        try:
            if ctype == 'add':
                mtype = params.pop('type')
                path = params.pop('path')
                if mtype in ('submenu', ):
                    name = params.pop('name', None)
                else:
                    name = params.pop('name')
                self.guimanager.AddItem(mtype, path, name, self._guiactivated, addr, **params)
                self.manager.Send(addr, RESP_GUI_ADDED, type = mtype, fullname = path + '/' + (name or ''))
            
            elif ctype == 'sensitive':
                self.guimanager.SetSensitive(params['path'], True)
                self.manager.Send(addr, RESP_GUI_SENSITIVE, path = params['path'])
            
            elif ctype == 'insensitive':
                self.guimanager.SetSensitive(params['path'], False)
                self.manager.Send(addr, RESP_GUI_INSENSITIVE, path = params['path'])
                
            else:
                self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'gui', type = ctype)
        except (KeyError, ), e:
            raise ParamMissingError(e.message)
        
    def _guiactivated(self, item, path, addr):
        print 'GuiActivated', path, addr
        self.manager.Send(addr, RESP_GUI_ACTIVATED, path = path)
