import socket
import thread
from ComSpec import *
from SocketWrapper import CSocketWrapper
from Future import CFuture
from ExceptionCarrier import CExceptionCarrier

class CConnection(object):
    
    def __init__(self, port):
        #~ try:
            self.lock = thread.allocate()
            self.lastid = 0
            self.results = {}
            sock = socket.socket()
            sock.connect(('', port))
            self.wrapper = CSocketWrapper(sock, self, None, False)
            self.guicallback = {}
        
        #~ except socket.error
    
    def Command(self, command, params, data, addr):
        try:
            print command, params, data, addr
            self.lock.acquire()
            code = int(command['code'])
            if 200 <= code <= 299 or 400 <= code <= 499:
                __id__ = params.pop('__id__', None)
                if __id__ is None:
                    return
                lck = self.results[__id__]
                
                if code in (RESP_METAMODEL_DESCRIPTION, RESP_RESULT):
                    self.results[__id__] = params['result']
                    
                elif code in (RESP_OK, RESP_GUI_ADDED, RESP_GUI_SENSITIVE, RESP_GUI_INSENSITIVE):
                    self.results[__id__] = True
                
                elif 400 <= code <= 499:
                    self.results[__id__] = CExceptionCarrier(Exception, *params.values())
                
                lck.release()
            elif code == RESP_GUI_ACTIVATED:
                path = params['path']
                if path in self.guicallback:
                    thread.start_new(self.guicallback[path], (path, ))
            
            
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