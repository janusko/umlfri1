from lib.Base import CBaseObject
from lib.FileTypes.FileType import CFileType

class CFileTypeManager(CBaseObject):
    _persistent = True
    
    def __init__(self):
        self.__fileTypes = []
    
    def GetFileType(self, mimeType):
        for fileType in self.__fileTypes:
            if fileType.GetMimeType() == mimeType:
                return fileType
        
        return None
    
    def GetFileTypes(self):
        for fileType in self.__fileTypes:
            yield fileType
    
    def RegisterFileType(self, mimeType, description):
        ret = CFileType(mimeType, description)
        self.__fileTypes.append(ret)
        return ret
