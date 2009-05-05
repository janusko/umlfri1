import socket
import thread
from ComSpec import *
from SocketWrapper import CSocketWrapper
from Future import CFuture

class CConnection(object):
    
    def __init__(self, port):
        #~ try:
            self.lock = thread.allocate()
            self.lastid = 0
            self.results = {}
            sock = socket.socket()
            sock.connect(('', port))
            self.wrapper = CSocketWrapper(sock, self, None, False)
        
        #~ except socket.error
    
    def Command(self, command, params, data, addr):
        try:
            print command, params, data, addr
            self.lock.acquire()
            code = int(command['code'])
            if 200 <= code <= 299:
                if '__id__' in params:
                    __id__ = params['__id__']
                else:
                    return
                lck = self.results[__id__]
                
                if code in (RESP_METAMODEL_DESCRIPTION, RESP_RESULT):
                    self.results[__id__] = params['result']
                    
                elif code in (RESP_OK, RESP_GUI_ADDED, RESP_GUI_SENSITIVE, RESP_GUI_INSENSITIVE):
                    self.results[__id__] = True
                
                lck.release()
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
