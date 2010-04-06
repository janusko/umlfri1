import thread, time, sys, socket, re
from lib.Depend.gtk2 import gtk
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Exceptions import *
from meta import Meta
from lib.Base import CBaseObject
from lib.Addons.Plugin.Communication.Encoding import *

class CCore(object):
    
    def __init__(self, manager, pluginAdapter):
        self.manager = manager
        self.pluginAdapter = pluginAdapter
        self.guimanager = manager.GetGuiManager()
    
    def GetGuiManager(self):
        return self.guimanager
    
    def Error(self, addr):
        pass
    
    def Stopped(self, id):
        return True
    
    def Command(self, command, params, data, addr):
        if command['version'] == VERSION:
            try:
                com = command['command'].lower()
                callid = params.pop('__id__', None)
                
                args = tuple(DecodeValue(i, True, self, addr) for i in t_eval(params['args']))
                kwds = dict((k, DecodeValue(v, True, self, addr)) for k, v in t_eval(params['kwds']).iteritems())
            
                if com == 'exec':
                    self._exec(command['type'], args, kwds, addr, callid)
                
                elif com == 'transaction':
                    self._transaction(command['type'], args, kwds, addr, callid)
                
                elif com == 'plugin':
                    self._plugin(command['type'], args, kwds, addr, callid)
                    
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
    
    def _transaction(self, com, args, kwds, addr, callid):
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
        
    
    def _exec(self, com, args, kwds, addr, callid):
        try:
            match = re.match(r'(?P<id>([#a-zA-Z_][-a-zA-Z0-9_]*)).(?P<fname>\w+)$', com)
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
                self.manager.GetTransaction(addr).Action(Meta.Execute, (obj, fname, args, kwds, self, addr))
            else:
                result = Meta.Execute(obj, fname, args, kwds, self, addr)
            
            result = EncodeValue(result, True, self, addr)
            
            self.manager.Send(addr, RESP_RESULT, __id__ = callid, result = result)
        
        except (UnknowMethodError, ), e:
            self.manager.Send(addr, RESP_UNKNOWN_METHOD, id = identifier, fname = fname, __id__ = callid)
        
        except (PluginInvalidMethodParameters, ), e:
            self.manager.Send(addr, RESP_INVALID_METHOD_PARAMETER, id = identifier, fname = fname, __id__ = callid)
            
        except (TypeError, ), e:
            raise ParamMissingError()
        
        except (ValueError, ), e:
            raise ParamValueError()
    
    def _plugin(self, ctype, args, kwds, addr, callid):
        if ctype == 'init':
            self.manager.ConnectPlugin(kwds['uri'], addr)
            self.manager.Send(addr, RESP_OK, __id__ = callid)
        else:
            self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'plugin', type = ctype, __id__ = callid)
    
    def _callback(self, id, addr, *args, **kwds):
        args = tuple(EncodeValue(i, True, self, addr) for i in args)
        kwds = dict((k, EncodeValue(v, True, self, addr)) for k, v in kwds.iteritems())
            
        self.manager.Send(addr, RESP_CALLBACK, callback = id, args = r_eval(args), kwds = r_eval(kwds))
            
