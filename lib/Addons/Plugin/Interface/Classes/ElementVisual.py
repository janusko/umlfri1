from VisibleObject import IVisibleObject
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Drawing.Diagram import CDiagram

class IElementVisual(IVisibleObject):
    __cls__ = CElement
    
    @result(r_objectlist)
    def GetConnections(him):
        return list(him.GetConnections())
    
