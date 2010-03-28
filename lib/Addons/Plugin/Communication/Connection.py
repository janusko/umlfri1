import socket
import thread
from ComSpec import *
from lib.Exceptions import *
from SocketWrapper import CSocketWrapper
from Future import CFuture
from ExceptionCarrier import CExceptionCarrier

class CConnection(object):
    
    def __init__(self, port):
        self.lock = thread.allocate()
        self.lastid = 0
        self.results = {}
        sock = socket.socket()
        sock.connect(('localhost', port))
        self.wrapper = CSocketWrapper(sock, self, None, False)
        self.guicallback = {}
        self.finalized = thread.allocate()
        self.finalized.acquire()
        
        self.callbacks = {}
        self.callbackidx = -1
        self.callbacklock = thread.allocate()
    
    def Command(self, command, params, data, addr):
        try:
            self.lock.acquire()
            code = int(command['code'])
            if 200 <= code <= 299 or 400 <= code <= 599:
                __id__ = params.pop('__id__', None)
                if __id__ is None:
                    return
                lck = self.results[__id__]
                
                if code in (RESP_METAMODEL_DESCRIPTION, RESP_RESULT):
                    self.results[__id__] = params['result']
                    
                elif code in (RESP_OK, RESP_GUI_ADDED, RESP_GUI_SENSITIVE, RESP_GUI_INSENSITIVE):
                    self.results[__id__] = True
                
                elif 400 <= code <= 599:
                    self.results[__id__] = CExceptionCarrier({
                        RESP_UNKONWN_COMMAND: PluginUnknownCommand,
                        RESP_UNSUPPORTED_VERSION: PluginUnsupportedVersion,
                        RESP_INVALID_COMMAND_TYPE: PluginInvalidCommandType,
                        RESP_MISSING_PARAMETER: PluginMissingParameter,
                        RESP_INVALID_PARAMETER: PluginInvalidParameter,
                        RESP_INVALID_OBJECT: PluginInvalidObject,
                        RESP_UNKNOWN_METHOD: PluginUnknownMethod,
                        RESP_INVALID_METHOD_PARAMETER: PluginInvalidMethodParameters,
                        RESP_PROJECT_NOT_LOADED: PluginProjectNotLoaded,
                        RESP_UNKNOWN_CONSTRUCTOR: PluginUnknownConstructor,
                        RESP_TRANSACTION_PENDING: TransactionPendingError,
                        RESP_OUT_OF_TRANSACTION: OutOfTransactionError,
                        RESP_TRANSACTION_MODE_UNSPECIFIED: TransactionModeUnspecifiedError,
                        RESP_UNHANDELED_EXCEPTION: UMLException,
                        }[code], 
                        *((code,) + tuple(params.values())))
                
                lck.release()
            elif code == RESP_GUI_ACTIVATED:
                path = params['path']
                if path in self.guicallback:
                    thread.start_new(self.guicallback[path], (path, ))
                    
            elif code == RESP_CALLBACK:
                thread.start_new(self.callbacks[int(params['callback'])], ())
            
            elif code == RESP_FINALIZE:
                self.finalized.release()
                
        finally:
            self.lock.release()
    
    def Stopped(self, addr):
        pass
    
    def Error(self, addr):
        return True #so that connection won't break
    
    def Execute(self, command, type, params):
        try:
            self.lock.acquire()
            self.lastid += 1
            __id__ = str(self.lastid)
            params['__id__'] = __id__
            lck = thread.allocate()
            lck.acquire()
            self.results[__id__] = lck
            self.wrapper.Send(command, type, params = params)
            return CFuture(self.results[__id__], self.results, __id__, self.lock)
        
        finally:
            self.lock.release()
    
    def SetGuiCallback(self, path, callback):
        try:
            self.lock.acquire()
            self.guicallback[path] = callback
        finally:
            self.lock.release()
    
    def SetCallback(self, fun):
        try:
            self.callbacklock.acquire()
            self.callbackidx += 1
            self.callbacks[self.callbackidx] = fun
            return self.callbackidx
        finally:
            self.callbacklock.release()
    
    
    def WaitTillClosed(self):
        self.finalized.acquire()
        self.finalized.release()
        return
