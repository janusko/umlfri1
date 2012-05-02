from SimpleContainer import CSimpleContainer
from lib.Math2D import Path, PathPartLine, PathPartMove
import math
from lib.Exceptions.UserException import *
from lib.datatypes import CColor

class CDiamond(CSimpleContainer):
    types = {
        'fill': CColor,
        'border': CColor
    }
    def __init__(self, fill = None, border = CColor("white")):
        CSimpleContainer.__init__(self)
        self.fill = fill
        self.border = border
    
    def GetResizable(self):
        return True, True

    def Paint(self, context):
        size = context.ComputeSize(self)
        shadowcolor = context.GetShadowColor()
        if shadowcolor is None:
            border, fill = self.GetVariables(context, 'border', 'fill')
        else:
            border, fill = None, shadowcolor
        
        canvas = context.GetCanvas()
        pos = context.GetPos()
        size = context.ComputeSize(self)
        
        corners = []
        (x, y), (w, h) = pos, size
        positions = (x, y + h//2), (x + w//2, y), (x + w, y + h//2), (x + w//2, y + h)
        oldpos = None
        
        for i, c in enumerate(positions):
            if i:
                corners.append(PathPartLine(oldpos, c))
            else:
                corners.append(PathPartMove(c))
            oldpos = c
        corners = Path.Join(corners).Flattern()
        corners.Close()
        canvas.DrawPath(corners, border, fill)
        
        if shadowcolor is not None:
            return
        
        CSimpleContainer.Paint(self, context)
