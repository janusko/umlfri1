import threading
import traceback
import types
from ..Interfaces.Adapter import IAdapter

class CPlugin(object):
    def __init__(self, channel, adapter):
        self.__channel = channel
        self.__adapter = adapter
        adapterInterface = IAdapter(self, adapter)
        self.__objects = { # TODO: replace with weakref.WeakValueDictionary
            adapterInterface.uid: adapterInterface
        }
        
        threading.Thread(target = self.__main).start()
    
    def __main(self):
        while True:
            data = self.__channel.ReadData()
            if self.__channel.IsClosed():
                return
            self.__execute(data)
    
    def __execute(self, data):
        session = data.get('session')
        try:
            obj = self.__objects[data['target']]
            selector = data['selector']
            args = data.get('args')
            
            method = getattr(obj, selector)
            
            args = self.__decodeParams(method, args)
            ret = method(**args)
            
            if session is not None:
                self.__channel.WriteData(
                    {
                        'session': session,
                        'return': self.__encodeReturn(method, ret)
                    }
                )
            
        except Exception, ex:
            if session is not None:
                self.__channel.WriteData(
                    {
                        'session': session,
                        'exception': self.__encodeException(ex)
                    }
                )
                # todo - remove
                traceback.print_exc()
            elif __debug__:
                traceback.print_exc()

    def __decodeParams(self, method, args):
        func = method.im_func
        if not hasattr(func, 'method_param_types'):
            return {}
        
        # ignore self parameter
        params = func.func_code.co_varnames[1:func.func_code.co_argcount + 1]
        paramtypes = func.method_param_types
        
        typedargs = {}
        
        for name, type in zip(params, paramtypes):
            value = args.pop(name)
            
            if type is object:
                if value is None:
                    typedargs[name] = None
                else:
                    # todo exception - object not found
                    typedargs[name] = self.__objects[value]
            elif type is None:
                vartype, value = value
                # todo exception - incorrect parameter type
                if vartype == "boolean":
                    typedargs[name] = value == "true"
                elif vartype == "int32":
                    typedargs[name] = int(value)
                elif vartype == "float":
                    typedargs[name] = float(value)
                elif vartype == "string":
                    typedargs[name] = str(value)
                else:
                    pass # todo exception - incorrect type
            elif type is bool:
                typedargs[name] = value == "true"
            else:
                # todo exception - incorrect parameter type
                typedargs[name] = type(value)
        
        # todo exception - some parameters left unprocessed
        
        return typedargs

    def __encodeReturnInternal(self, ret, polymorfic):
        if hasattr(ret, '__iter__'):
            return [self.__encodeReturnInternal(value, polymorfic) for value in ret]
        elif hasattr(ret, 'uid'):
            if ret.uid not in self.__objects:
                self.__objects[ret.uid] = ret
            if polymorfic:
                return (ret.__class__.__name__, ret.uid)
            else:
                return ret.uid
        else:
            return ret
    
    def __encodeReturn(self, method, ret):
        polymorfic = hasattr(method, 'method_polymorfic')
        
        return self.__encodeReturnInternal(ret, polymorfic)
    
    def __encodeException(self, ex):
        return {'type': ex.__class__.__name__}
    
    def GetTransaction(self):
        pass
    
    def RelativePath2Absolute(self, path):
        pass
    
    def GetAdapter(self):
        return self.__adapter
    
    def SendStop(self):
        pass # TODO: send stop to plugin
