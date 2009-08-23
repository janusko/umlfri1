from VisualObject import CVisualObject

from lib.Exceptions.UserException import *
from math import pi, atan2

from lib.Math2D import Path, TransformMatrix
from lib.datatypes import CColor

from lib.config import config

arrows = {
    "simple": "M -0.5,-1 L 0,0 L 0.5,-1",
    "triangle": "M -0.5,-1 L 0,0 L 0.5,-1 z",
    "diamond": "M -0.5,-1 L 0,0 L 0.5,-1 L 0,-2 z"
}

class CConnectionArrow(CVisualObject):
    types = {
        'index': int,
        'direction': str,
        'style': str,
        'color': CColor,
        'fill': CColor,
        'size': int
    }
    def __init__(self, index, direction = None, style = 'simple', color = CColor('black'), fill = None, size = 10):
        CVisualObject.__init__(self)
        
        assert direction in (None, 'rev', 'fwd')
        
        self.style = style
        self.fill = fill
        self.size = size
        self.color = color
        self.index = index
        self.direction = direction

    def ComputeSize(self, context):
        return 0, 0

    def Paint(self, context):
        index, direction, style, fill, size, color = self.GetVariables(context, 'index', 'direction', 'style', 'fill', 'size', 'color')
        
        if direction is None:
            if index == 0:
                direction = 'rev'
            else:
                direction = 'fwd'
        
        points = list(context.GetPoints())
        last = len(points) - 1
        
        if index > last or (direction == 'rev' and index == last):
            return
        
        if direction == 'fwd':
            Xangle = points[index][0] - points[index-1][0]
            Yangle = points[index][1] - points[index-1][1]
        else:
            Xangle = points[index][0] - points[index+1][0]
            Yangle = points[index][1] - points[index+1][1]
        
        angle = atan2(-Xangle, Yangle)
        
        steps = config['/Styles/Connection/ArrowAngleSteps']
        step = 2 * pi / steps
        angle = step * ( (angle // step + (1 if angle % step / step > .5 
                          else 0)) % steps )
        
        transMatrix = TransformMatrix.mk_translation(points[index])*TransformMatrix.mk_rotation(angle)* \
                        TransformMatrix.mk_scale(size)
        
        arrow = transMatrix*Path(arrows.get(style, style))
        context.GetCanvas().DrawPath(arrow, color, fill)
