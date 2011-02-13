from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Connections.Type import CConnectionType

class IConnectionType(IBase):
    __cls__ = CConnectionType
    
    def GetName(him):
        return him.GetId()
    
    def GetDomain(him):
        return him.GetDomain()
    
    def GetIdentity(him):
        return him.GetConnectionIdentity()
    
    def HasIdentity(him):
        return him.GetConnectionIdentity() is not None
        
