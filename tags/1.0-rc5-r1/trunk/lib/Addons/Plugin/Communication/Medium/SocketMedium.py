import socket
from MediumTimeout import MediumTimeout
from MediumError import MediumError

class CSocketMedium(object):
    
    def __init__(self, item):
        if isinstance(item, (int, long)):
            self.__sock = socket.socket()
            self.__sock.connect(('localhost', item))
        elif isinstance(item, socket._socketobject):
            self.__sock = item
        self.__sock.settimeout(1.)
        self.__isOpened = not self._isClosedSocket()
        
    def _isClosedSocket(self):
        return isinstance(self.__sock._sock, socket._closedsocket)
    
    def IsOpened(self):
        return self.__isOpened and not self._isClosedSocket()
        
    def Recv(self, buflen):
        try:
            if self.__isOpened:
                data = self.__sock.recv(buflen)
                if data == '':
                    self.__isOpened = False
                return data
            else:
                return ''
            
        except socket.timeout:
            raise MediumTimeout()
        
        except socket.error:
            self.__isOpened = False
            raise MediumError()
    
    def Send(self, buffer):
        try:
            self.__sock.sendall(buffer)
        
        except socket.timeout:
            raise MediumTimeout()
            
        except socket.error:
            self.__isOpened = False
            raise MediumError()
    
    def Close(self):
        if self.IsOpened():
            self.__sock.close()
            self.__isOpened = False
