from VisibleObject import IVisibleObject
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Drawing.Diagram import CDiagram

class IElementVisual(IVisibleObject):
    __cls__ = CElement
    
    @result(r_objectlist)
    def GetConnections(him):
        return list(him.GetConnections())
    
    #~ @parameter('diagram', t_classobject(CDiagram))
    #~ @parameter('obj', t_classobject(CElementObject))
    #~ @parameter('pos', t_2intTuple)
    #~ @constructor
    #~ def Create(diagram, obj, pos):
        #~ if diagram is None or obj is None:
            #~ raise ValueError()
        #~ res = CElement(diagram, obj)
        #~ res.SetPosition(pos)
        #~ return res
    