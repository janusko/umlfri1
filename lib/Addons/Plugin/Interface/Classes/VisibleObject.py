from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IVisibleObject(IBase):
    __cls__ = None
    
    def GetPosition(him):
        return him.GetPosition()
    
    def GetCenter(him):
        return him.GetCenter()
    
    def GetSize(him):
        return him.GetSize()
    
    def GetMinimalSize(him):
        return him.GetMinimalSize()
    
    def GetSquare(him):
        return him.GetSquare()
        
    def AreYouAtPosition(him, pos):
        return him.AreYouAtPosition(pos)
    
    def AreYouInRange(him, topLeft, bottomRight, includeAll = True):
        return him.AreYouInRange(topLeft, bottomRight, includeAll)
    
    def GetObject(him):
        return him.GetObject()
    
    def GetDiagram(him):
        return him.GetDiagram()
    
    
