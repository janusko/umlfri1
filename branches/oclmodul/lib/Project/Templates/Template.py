from lib.Base import CBaseObject

class CTemplate(CBaseObject):
    _persistent = True
    
    def __init__(self, name, storage, path, icon, metamodelUri = None):
        self.__name = name
        self.__storage = storage
        self.__path = path
        self.__icon = icon
        self.__metamodelUri = metamodelUri
    
    def GetStorage(self):
        return self.__storage
    
    def GetIcon(self):
        return self.__icon
    
    def GetName(self):
        return self.__name
    
    def GetMetamodelUri(self):
        return self.__metamodelUri
    
    def LoadInto(self, project):
        project.LoadProject(self.__path, True, self.__storage)
