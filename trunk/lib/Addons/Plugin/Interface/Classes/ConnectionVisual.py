from base import IBase
from lib.Drawing.Connection import CConnection
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import *

class IConnectionVisual(IBase):
    __cls__ = CConnection
    
    def GetObject(him):
        return him.GetObject()
    
    def GetDestination(him):
        return him.GetDestination()
    
    def GetSource(him):
        return him.GetSource()
    
    def GetPoints(him):
        return list(him.GetPoints(IBase.adapter.GetCanvas()))
        
    def GetAllLabelPositions(him):
        return list(him.GetAllLabelPositions())
    
    def GetDiagram(him):
        return him.GetDiagram()
    
    
