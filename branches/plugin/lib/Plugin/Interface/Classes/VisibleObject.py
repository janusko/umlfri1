from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *

class IVisibleObject(IBase):
    __cls__ = None
    
    @result(r_2intTuple)
    def GetPosition(him):
        return him.GetPosition(IBase.adapter.GetCanvas())
    
    @result(r_2intTuple)
    def GetCenter(him):
        return him.GetCenter(IBase.adapter.GetCanvas())
    
    @result(r_2intTuple)
    def GetSize(him):
        return him.GetSize(IBase.adapter.GetCanvas())
    
    @result(r_2intTuple)
    def GetMinimalSize(him):
        return him.GetMinimalSize(IBase.adapter.GetCanvas())
    
    @result(r_2x2intTuple)
    def GetSquare(him):
        return him.GetSquare(IBase.adapter.GetCanvas())
        
    @parameter('pos', t_2intTuple)
    @result(r_bool)
    def AreYouAtPosition(him, pos):
        return him.AreYouAtPosition(IBase.adapter.GetCanvas(), pos)
    
    @parameter('topleft', t_2intTuple)
    @parameter('bottomright', t_2intTuple)
    @parameter('all', t_bool)
    @result(r_bool)
    def AreYouInRange(him, topleft, bottomright, all = False):
        return him.AreYouInRange(IBase.adapter.GetCanvas(), topleft, bottomright, all)
    
    @result(r_object)
    def GetObject(him):
        return him.GetObject()
    
    @result(r_object)
    def GetDiagram(him):
        return him.GetDiagram()
    
    #~ @parameter('pos', t_2intTuple)
    #~ @result(r_none)
    #~ def SetPosition(him, pos):
        #~ him.SetPosition(pos, IBase.adapter.GetCanvas())
    
