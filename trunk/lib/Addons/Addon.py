class CAddon(object):
    def __init__(self, storage, uri, component, name, version = None, icon = None):
        self.__storage = storage
        self.__uri = uri
        
        self.__component = component
        component._SetAddon(self)
        
        self.__name = name
        self.__version = version
        
        self.__icon = icon
    
    def GetStorage(self):
        return self.__storage
    
    def GetUri(self):
        return self.__uri
    
    def GetName(self):
        return self.__name
    
    def GetVersion(self):
        return self.__version
    
    def GetComponent(self):
        return self.__component
    
    def GetType(self):
        return self.__component.GetType()
    
    def GetIcon(self):
        return self.__icon
