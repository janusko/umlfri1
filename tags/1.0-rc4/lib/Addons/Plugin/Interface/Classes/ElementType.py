from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Elements.Type import CElementType
from lib.Connections.Type import CConnectionType

class IElementType(IBase):
    __cls__ = CElementType
    
    def GetName(him):
        return him.GetId()
    
    def GetDomain(him):
        return him.GetDomain()
    
    def GetIdentity(him):
        return him.GetIdentity()
    
    def GetConnections(him):
        cf = him.GetMetamodel().GetConnectionFactory()
        return [cf.GetConnection(i[0]) for i in him.GetConnections()]
    
    def ConnectWith(him, connection):
        return him.connections[connection.GetId()][0] or []
    
    def AllowedRecursive(him, connection):
        return him.connections[connection.GetId()][1]
        
#todo: remake GetConnections and add GetOptions
