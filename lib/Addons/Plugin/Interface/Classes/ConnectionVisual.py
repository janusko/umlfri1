from base import IBase
from lib.Drawing.Connection import CConnection
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import *

class IConnectionVisual(IBase):
    __cls__ = CConnection
    
    @result(r_object)
    def GetObject(him):
        return him.GetObject()
    
    @result(r_object)
    def GetDestination(him):
        return him.GetDestination()
    
    @result(r_object)
    def GetSource(him):
        return him.GetSource()
    
    @result(r_object)
    def GetDestinationObject(him):
        return him.GetDestinationObject()
    
    @result(r_object)
    def GetSourceObject(him):
        return him.GetSourceObject()
    
