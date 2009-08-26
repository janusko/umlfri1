from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Elements.Type import CElementType
from lib.Connections.Type import CConnectionType

class IElementType(IBase):
    __cls__ = CElementType
    
    @result(r_str)
    def GetName(him):
        return him.GetId()
    
    @result(r_object)
    def GetDomain(him):
        return him.GetDomain()
    
    @result(r_str)
    def GetIdentity(him):
        return him.GetIdentity()
    
    @result(r_bool)
    def HasIdentity(him):
        return him.GetIdentity() is not None
        
    @result(r_objectlist)
    def GetConnections(him):
        cf = him.GetMetamodel().GetConnectionFactory()
        return [cf.GetConnection(i[0]) for i in him.GetConnections()]
    
    @parameter('connection', t_classobject(CConnectionType))
    @result(r_objectlist)
    def ConnectWith(him, connection):
        return him.connections[connection.GetId()][0] or []
    
    @parameter('connection', t_classobject(CConnectionType))
    @result(r_bool)
    def AllowedRecursive(him, connection):
        return him.connections[connection.GetId()][1]
    
    @result(r_2boolTuple)
    def GetResizable(him):
        return him.GetResizable()
        
#todo: remake GetConnections and add GetOptions
