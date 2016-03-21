from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Domains.Type import CDomainType

class IDomainType(IBase):
    __cls__ = CDomainType
    
    def GetName(him):
        return him.GetName()
    
