import os

from .FileChannel import CFileChannel

class CPipeChannel(CFileChannel):
    def __init__(self):
        readMy, writeOthers = os.pipe()
        readOthers, writeMy = os.pipe()
        
        CFileChannel.__init__(self, os.fdopen(readMy, 'r'), os.fdopen(writeMy, 'w'))
        
        self.__readOthers = readOthers
        self.__writeOthers = writeOthers
    
    def GetReaderFD(self):
        return self.__readOthers
    
    def GetWriterFD(self):
        return self.__writeOthers
