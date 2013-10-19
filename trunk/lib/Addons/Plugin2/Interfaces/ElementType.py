from ..PluginBase import params, mainthread, polymorphic

from . import ConnectionType

class IElementType(object):
    def __init__(self, elementType):
        self.__elementType = elementType
    
    @property
    def _elementType(self):
        return self.__elementType
    
    def GetName(self):
        return self.__elementType.GetId()
    
    def GetDomain(self):
        return self.__elementType.GetDomain()
    
    def GetIdentity(self):
        return self.__elementType.GetIdentity()
    
    def GetConnections(self):
        cf = self.__elementType.GetMetamodel().GetConnectionFactory()
        for connection in self.__elementType.GetConnections():
            yield ConnectionType.IConnectionType(connection)
    
    @params(object)
    def ConnectedWith(self, connection):
        return self.__elementType.connections[connection._connectionType.GetId()][0] or []
    
    @params(object)
    def AllowedRecursive(self, connection):
        return self.__elementType.connections[connection._connectionType.GetId()][1]
