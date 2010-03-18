from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Metamodel.Metamodel import CMetamodel

class IMetamodel(IBase):
    __cls__ = CMetamodel
    
    @result(r_str)
    def GetUri(him):
        return him.GetUri()
    
    @result(r_str)
    def GetVersion(him):
        return him.GetVersion()
        
    @result(r_objectlist)
    def GetDiagrams(him):
        return list(him.GetDiagramFactory())
    
    @result(r_objectlist)
    def GetElements(him):
        return list(him.GetElementFactory().IterTypes())
    
    @result(r_objectlist)
    def GetConnections(him):
        return list(him.GetConnectionFactory().IterTypes())
    
    @result(r_objectlist)
    def GetDomains(him):
        return list(him.GetDomainFactory().IterTypes())
        
