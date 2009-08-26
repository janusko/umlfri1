from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Connections.Type import CConnectionType

class IConnectionType(IBase):
    __cls__ = CConnectionType
    
    @result(r_str)
    def GetName(him):
        return him.GetId()
    
    @result(r_object)
    def GetDomain(him):
        return him.GetDomain()
    
    @result(r_str)
    def GetIdentity(him):
        return him.GetConnectionIdentity()
    
    @result(r_bool)
    def HasIdentity(him):
        return him.GetConnectionIdentity() is not None
        
