import os
from MediumTimeout import MediumTimeout
from MediumError import MediumError

class CPipeMedium(object):
    
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
            
    def IsOpened(self):
        return self.__isOpened and not self._isClosedPipe()
        
    def Recv(self, buflen):
        try:
            if self.__isOpened:
                data = os.read(self.__fr, buflen)
                if data == '':
                    self.__isOpened = False
                return data
            else:
                return ''
        
        except OSError:
            self.__isOpened = False
            raise MediumError()
        
    def Send(self, buffer):
        try:
            if self.__isOpened:
                os.write(self.__fw, buffer)
            else:
                raise MediumError()
        
        except OSError:
            self.__isOpened = False
            raise MediumError()
    
    def Close(self):
        try:
            os.close(self.__fw)
        except OSError:
            pass
        
        try:
            os.close(self.__fr)
        except OSError:
            pass
            
        
        self.__isOpened = False
