import socket
import thread
import ComSpec
from ComSpec import *
from Encoding import *
from lib.Exceptions import *
from SocketWrapper import CSocketWrapper
from Future import CFuture
from ExceptionCarrier import CExceptionCarrier

class CConnection(object):
    
    def __init__(self, port, mainloop):
        self.lock = thread.allocate()
        self.lastid = 0
        self.results = {}
        sock = socket.socket()
        sock.connect(('localhost', port))
        self.wrapper = CSocketWrapper(sock, self, None, False)
        self.guicallback = {}
        self.mainloop = mainloop
        
        self.callbacks = {}
        self.callbackidx = -1
        self.callbacklock = thread.allocate()
    
    def SetMainloop(self, mainloop):
        self.mainloop = mainloop
    
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
                    self.results[__id__] = CExceptionCarrier(code2Exception[code], 
                        *((code,) + tuple(params.values())))
                
                lck.release()
            elif code == RESP_GUI_ACTIVATED:
                path = params['path']
                if path in self.guicallback:
                    self.mainloop.Call(self.guicallback[path], path)
                    
            elif code == RESP_CALLBACK:
                args = t_eval(params['args'])
                kwds = t_eval(params['kwds'])
                
                args = tuple(DecodeValue(i, False, self) for i in args)
                kwds = dict((k, DecodeValue(v, False, self)) for k, v in kwds.iteritems())
                    
                callback = self.callbacks[int(params['callback'])]
                self.mainloop.Call(callback, *args, **kwds)
            
            elif code == RESP_FINALIZE:
                self.mainloop.Stop()
                
        finally:
            self.lock.release()
    
    def Stopped(self, addr):
        pass
    
    def Error(self, addr):
        return True #so that connection won't break
    
    def Execute(self, command, type, args, kwds):
        try:
            self.lock.acquire()
            self.lastid += 1
            __id__ = str(self.lastid)
            lck = thread.allocate()
            lck.acquire()
            self.results[__id__] = lck
            self.wrapper.Send(command, type, {'__id__': __id__, 'args': r_eval(args), 'kwds': r_eval(kwds)})
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
            if hasattr(fun, 'im_func'):
                ff = fun.im_func
            else:
                ff = fun
            if not hasattr(ff, '_callbackId'):
                self.callbackidx += 1
                ff._callbackId = self.callbackidx
                self.callbacks[self.callbackidx] = fun
            return ff._callbackId
        finally:
            self.callbacklock.release()
    