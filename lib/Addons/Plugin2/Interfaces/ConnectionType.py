from ..PluginBase import params, mainthread, polymorphic

class IConnectionType(object):
    def __init__(self, connectionType):
        self.__connectionType = connectionType
    
    @property
    def _connectionType(self):
        return self.__connectionType
    
    def GetName(self):
        return self.__connectionType.GetId()
    
    def GetDomain(self):
        return self.__connectionType.GetDomain()
