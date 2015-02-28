class CUpdateResponse(object):
    def __init__(self,addon,uri):
        self.__addon = addon
        self.__uri = uri
        
    def GetAddon(self):
        return self.__addon
    
    def GetUri(self):
        return self.__uri
