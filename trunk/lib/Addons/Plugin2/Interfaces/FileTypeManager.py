from .Decorators import params, mainthread, polymorphic

from lib.Addons.Plugin2.Interfaces import FileType

class IFileTypeManager(object):
    def __init__(self, manager):
        self.__manager = manager
    
    @params(str, str)
    def RegisterFileType(self, mimeType, description):
        return FileType.IFileType(self.__manager.RegisterFileType(mimeType, description))
