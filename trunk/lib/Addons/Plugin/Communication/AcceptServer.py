import thread, socket
from lib.Addons.Plugin.Communication.Medium import CSocketMedium


class CAcceptServer(object):
    '''
    Client-side communication part of application
    '''
    
    def __init__(self, addr, callback):
        '''
        @param addr: 2-tuple address of iface to bind listening socket to
        @type addr: 2-tuple
        @param callback: callable function:
            
            - accepts two parameters: connected socket object and address tuple
            - mustn't block, so that accept server can continue
        '''
        self.run = None
        self.addr = addr
        self.callback = callback
        
    def Start(self):
        '''
        @return: True on success, False otherwise
        
        starts accept server in separate thread
        '''
        if self.run:
            return True
        try:
            self.sock = socket.socket()
            self.sock.settimeout(1.)
            self.sock.bind(self.addr)
            self.sock.listen(1)
            self.run = True
            thread.start_new(self._server, ())
        
        except socket.error:
            return False
        
        else:
            return True
    
    def Stop(self):
        '''
        Make server thread stop its activity.
        Action is asynchronous, server will stop after short period of time.
        '''
        if self.run:
            self.run = False
    
    def IsActive(self):
        '''
        @return: True if server thread appear to be running
        '''
        return self.run is not None
    
    def _server(self):
        '''
        Main of server thread
        every new connection is directed to callback function
        '''
        try:
            while self.run:
                try:
                    sock, addr = self.sock.accept()
                    if self.run:
                        self.callback(CSocketMedium(sock), addr)
                    else:
                        sock.close()
                    
                except socket.timeout:
                    continue
        finally:
            self.run = None
            self.sock.close()
    
    def GetPort(self):
        if self.run:
            return self.sock.getsockname()[1]
        else:
            return None
