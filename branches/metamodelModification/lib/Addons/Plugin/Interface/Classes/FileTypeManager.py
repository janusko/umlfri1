import lib.GenericGui
from base import IBase

class IFileTypeManager(IBase):
    
    __cls__ = lib.GenericGui.CFileTypeManager
    
    def RegisterFileType(him, mimeType, description):
        return him.RegisterFileType(mimeType, description)
