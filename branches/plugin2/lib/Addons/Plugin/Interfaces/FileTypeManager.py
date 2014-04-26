from .Decorators import params, mainthread, polymorphic

from lib.Addons.Plugin.Interfaces import FileType

class IFileTypeManager(object):
    def __init__(self, manager):
        self.__manager = manager
    
    @property
    def uid(self):
        return self.__manager.GetUID()
    
    @params(str, str)
    def RegisterFileType(self, mimeType, description):
        return FileType.IFileType(self.__manager.RegisterFileType(mimeType, description))
