from SimpleContainer import CSimpleContainer
from lib.Math2D import Path, PathPartLine, PathPartMove, TransformMatrix
import math
from lib.Exceptions.UserException import *
from lib.datatypes import CColor

cornerDefs = {
    'rounded': 'M 0,1 C 0,0.446 0.446,0 1,0',
    'note': 'M 0,1 L 1,1 L 1,0 L 0,1 z  M 0,1 L 1,0',
}

sideDefs = {
    'rounded': 'M 0,0 C -0.554,0 -1,-0.223 -1,-0.5 C -1,-0.777 -0.554,-1 0,-1',
}

class CRectangle(CSimpleContainer):
    types = {
        'fill': CColor,
        'border': CColor,
        'lefttop': str,
        'righttop': str,
        'leftbottom': str,
        'rightbottom': str,
        'left': str,
        'right': str,
        'top': str,
        'bottom': str
    }
    def __init__(self, fill = None, border = CColor("white"), lefttop = None, righttop = None, leftbottom = None, rightbottom = None, left = None, right = None, top = None, bottom = None):
        CSimpleContainer.__init__(self)
        self.fill = fill
        self.border = border
        
        self.lefttop, self.righttop, self.rightbottom, self.leftbottom = lefttop, righttop, rightbottom, leftbottom
        self.top, self.right, self.bottom, self.left = top, right, bottom, left
        
        if top is not None:
            if lefttop is not None or righttop is not None:
                raise XMLError("Rectangle", "top")
        if bottom is not None:
            if leftbottom is not None or rightbottom is not None:
                raise XMLError("Rectangle", "bottom")
        if left is not None:
            if lefttop is not None or leftbottom is not None:
                raise XMLError("Rectangle", "left")
        if right is not None:
            if righttop is not None or rightbottom is not None:
                raise XMLError("Rectangle", "right")
    
    def GetResizable(self):
        return True, True

    def Paint(self, context):
        size = context.ComputeSize(self)
        shadowcolor = context.GetShadowColor()
        if shadowcolor is None:
            border, fill = self.GetVariables(context, 'border', 'fill')
        else:
            border, fill = None, shadowcolor
        
        corners = []
        for i, c in enumerate(self.GetVariables(context, 'lefttop', 'righttop', 'rightbottom', 'leftbottom')):
            if c is not None:
                if isinstance(c, (str, unicode)):
                    c = c.split(None, 2)
                if len(c) == 2:
                    c = c[0], None, c[1]
                trans = TransformMatrix.mk_scale(int(c[0]))*TransformMatrix.mk_rotation(i*math.pi/2)
                c = str(c[1]), trans*Path(cornerDefs.get(c[2], c[2]))
            corners.append(c)
        
        sides = []
        for i, s in enumerate(self.GetVariables(context, 'top', 'right', 'bottom', 'left')):
            if s is not None:
                if isinstance(s, (str, unicode)):
                    s = s.split(None, 2)
                if len(s) == 2:
                    s = s[0], None, s[1]
                trans = TransformMatrix.mk_rotation((i+1)*math.pi/2)
                s = str(s[1]), trans*Path(sideDefs.get(s[2], s[2])), int(s[0])
            sides.append(s)
        
        canvas = context.GetCanvas()
        pos = context.GetPos()
        size = context.ComputeSize(self)
        
        if sides == corners == (None, None, None, None):
            canvas.DrawRectangle(pos, size, border, fill)
        else:
            cornerPath = []
            (x, y), (w, h) = pos, size
            if sides[0] is not None:
                y += sides[0][2]
                h -= sides[0][2]
            if sides[1] is not None:
                w -= sides[1][2]
            if sides[2] is not None:
                h -= sides[2][2]
            if sides[3] is not None:
                x += sides[3][2]
                w -= sides[3][2]
            positions = (x, y), (x + w, y), (x + w, y+h), (x, y+h)
            oldpos = None
            lastside = None
            for i, c in enumerate(corners):
                if c is None:
                    if sides[i] is not None:
                        scale = ((w, ides[i][2]), (sides[i][2], h), (w, sides[i][2]), (sides[i][2], h))
                        if i == 3 and lastside is not None:
                            tmp = lastside
                        else:
                            tmp = TransformMatrix.mk_translation(positions[i])*TransformMatrix.mk_scale2(scale[i])*sides[i][1][-1]
                        if sides[i-1] is None:
                            if i:
                                cornerPath.append(PathPartLine(oldpos, tmp.GetFirstPos()))
                            else:
                                cornerPath.append(PathPartMove(tmp.GetFirstPos()))
                        cornerPath.append(tmp)
                        oldpos = tmp.GetLastPos()
                    elif sides[i-1] is not None:
                        if not i:
                            scale = ((w, sides[i-1][2]), (sides[i-1][2], h), (w, sides[i-1][2]), (sides[i-1][2], h))
                            lastside = TransformMatrix.mk_translation(positions[i-1])*TransformMatrix.mk_scale2(scale[i-1])*sides[i-1][1][-1]
                            oldpos = lastside.GetLastPos()
                    else:
                        if i:
                            cornerPath.append(PathPartLine(oldpos, positions[i]))
                        else:
                            cornerPath.append(PathPartMove(positions[i]))
                        oldpos = positions[i]
                else:
                    tmp = TransformMatrix.mk_translation(positions[i])*c[1][-1]
                    cornerPath.append(tmp)
                    oldpos = tmp.GetLastPos()
            cornerPath = Path.Join(cornerPath).Flattern()
            cornerPath.Close()
            canvas.DrawPath(cornerPath, border, fill)
        
        if shadowcolor is not None:
            return
        
        CSimpleContainer.Paint(self, context)
        
        for i, c in enumerate(corners):
            if c is not None and len(c[1]) > 0:
                tmp = TransformMatrix.mk_translation(positions[i])*c[1][:-1]
                canvas.DrawPath(tmp, border, c[0])
        
        for i, s in enumerate(sides):
            if s is not None and len(s[1]) > 0:
                tmp = TransformMatrix.mk_translation(positions[i])*s[1][:-1]
                canvas.DrawPath(tmp, border, s[0])
