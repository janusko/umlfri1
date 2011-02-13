from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IVisibleObject(IBase):
    __cls__ = None
    
    def GetPosition(him):
        return him.GetPosition(IBase.adapter.GetCanvas())
    
    def GetCenter(him):
        return him.GetCenter(IBase.adapter.GetCanvas())
    
    def GetSize(him):
        return him.GetSize(IBase.adapter.GetCanvas())
    
    def GetMinimalSize(him):
        return him.GetMinimalSize(IBase.adapter.GetCanvas())
    
    def GetSquare(him):
        return him.GetSquare(IBase.adapter.GetCanvas())
        
    def AreYouAtPosition(him, pos):
        return him.AreYouAtPosition(IBase.adapter.GetCanvas(), pos)
    
    def AreYouInRange(him, topleft, bottomright, all = False):
        return him.AreYouInRange(IBase.adapter.GetCanvas(), topleft, bottomright, all)
    
    def GetObject(him):
        return him.GetObject()
    
    def GetDiagram(him):
        return him.GetDiagram()
    
    
