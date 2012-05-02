class CDependency(object):
    def __init__(self, uri, required = False, versionRange = None):
        self.__uri = uri
        self.__required = required
        self.__versionRange = versionRange
    
    def GetUri(self):
        return self.__uri
    
    def GetRequired(self):
        return self.__required
    
    def GetVersionRange(self):
        return self.__versionRange
