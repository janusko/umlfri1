from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Drawing.Element import CElement

class IElementVisual(IBase):
    __cls__ = CElement
    
    def GetPosition(self):
        return self.GetPosition()
    
    @parameter('pos', t_2intTuple)
    def SetPosition(self, pos):
        self.SetPosition(pos)
