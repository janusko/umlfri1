from DomainObject import IDomainObject
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Connections import CConnectionObject
from lib.Elements import CElementObject

class IConnectionObject(IDomainObject):
    __cls__ = CConnectionObject
    
    def GetConnectedObject(him, obj):
        return self.GetConnectedObject(obj)
        
    def GetDestination(him):
        return him.GetDestination()
    
    def GetSource(him):
        return him.GetSource()
    
