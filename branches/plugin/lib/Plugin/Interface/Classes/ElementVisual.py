from lib.Plugin.ComSpec import *
from lib.Plugin.Interface.meta import Meta
from lib.Plugin.Interface.decorators import *
from lib.Drawing.Element import CElement

class CElementVisual(object):
    __metaclass__ = Meta
    __cls__ = CElement
    
    def GetPosition(self):
        return self.GetPosition()
    
    @parameter('pos', t_2intTuple)
    def SetPosition(self, pos):
        self.SetPosition(pos)
