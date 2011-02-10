import os
from mediumTimeout import MediumTimeout
from mediumError import MediumError

class PipeMedium(object):
    
    def __init__(self, fr, fw):
        self.__fr = fr
        self.__fw = fw
        self.__isOpened = not self._isClosedPipe()
        
    def _isClosedPipe(self):
        try:
            os.fstat(self.__fr)
            os.fstat(self.__fw)
            return False
        except OSError:
            return True
            
    def isOpened(self):
        return self.__isOpened and not self._isClosedSocket()
        
    def recv(self, buflen):
        try:
            if self.__isOpened:
                data = os.read(self.__fw, buflen)
                if data == '':
                    self.__isOpened = False
                return data
        
        except OSError:
            self.__isOpened = False
            raise MediumError()
        
    def send(self, buffer):
        try:
            if self.__isOpened:
                os.write(self.__fw, buffer)
            else:
                raise MediumError()
        
        except OSError:
            self.__isOpened = False
            raise MediumError()
    
    def close(self):
        try:
            os.close(self.__fr)
        except OSError:
            pass
            
        try:
            os.close(self.__fw)
        except OSError:
            pass
        
        self.__isOpened = False
