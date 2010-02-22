class CTemplate(object):
    def __init__(self, name, storage, path, icon):
        self.__name = name
        self.__storage = storage
        self.__path = path
        self.__icon = icon
    
    def GetStorage(self):
        return self.__storage
    
    def GetIcon(self):
        return self.__icon
    
    def GetName(self):
        return self.__name
    
    def LoadInto(self, project):
        project.LoadProject(self.__path, True, self.__storage)
