from DomainObject import IDomainObject
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Connections import CConnectionObject
from lib.Elements import CElementObject

class IConnectionObject(IDomainObject):
    __cls__ = CConnectionObject
    
    @parameter('obj', t_classobject(CElementObject))
    @result(r_object)
    def GetConnectedObject(him, obj):
        return self.GetConnectedObject(obj)
        
    @result(r_object)
    def GetDestination(him):
        return him.GetDestination()
    
    @result(r_object)
    def GetSource(him):
        return him.GetSource()
    
