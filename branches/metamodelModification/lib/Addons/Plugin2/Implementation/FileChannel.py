import json
import threading
import traceback


class CFileChannel(object):
    __encoder = json.JSONEncoder(ensure_ascii = False, check_circular = False, allow_nan = False, encoding = "ascii")
    __decoder = json.JSONDecoder()
    
    def __init__(self, input, output):
        self.__input = input
        self.__output = output
        self.__writeLock = threading.Lock()
        
        self.__closed = False
    
    def WriteData(self, data):
        with self.__writeLock:
            if self.__closed:
                raise ValueError("I/O operation on closed file")
            
            for chunk in self.__encoder.iterencode(data):
                self.__output.write(chunk.encode('utf8'))
            self.__output.write('\r\n')
            self.__output.flush()
    
    def ReadData(self):
        if self.__closed:
            raise ValueError("I/O operation on closed file")
        
        while True:
            try:
                ret = self.__input.readline()
                if ret:
                    return self.__decoder.decode(ret.rstrip('\r\n').decode('utf8'))
            except:
                traceback.print_exc()
        
        self.__closed = True
    
    def Close(self):
        self.__input.close()
        self.__output.close()
    
    def IsClosed(self):
        return self.__closed
