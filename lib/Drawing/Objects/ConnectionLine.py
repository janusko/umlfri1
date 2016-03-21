from VisualObject import CVisualObject

from lib.datatypes import CColor

from lib.Math2D import CLine

class CConnectionLine(CVisualObject):
    types = {
        'color': CColor,
        'style': str,
        'width': int,
        'begin': float,
        'end': float,
    }
    def __init__(self, color = CColor('black'), style = 'solid', width = 1, begin = 0, end = 1):
        CVisualObject.__init__(self)
        
        self.color = color
        self.style = style
        self.width = width
        self.begin = begin
        self.end = end

    def ComputeSize(self, context):
        return 0, 0

    def Paint(self, context):
        color, style, width, begin, end = self.GetVariables(context, 'color', 'style', 'width', 'begin', 'end')
        
        if context.GetShadowColor() is not None:
            color = context.GetShadowColor()
        
        points = context.GetPoints()
        
        if begin > 0 or end < 1:
            if begin < 0:
                begin = 0
            
            if end > 1:
                end = 1
            
            lengths = []
            points = list(points)
            
            oldpoint = None
            length = 0
            
            for point in points:
                if oldpoint is not None:
                    length += abs(CLine(oldpoint, point))
                    lengths.append(length)
                
                oldpoint = point
            
            lastlength = lengths[-1]
            lengths = [length/lastlength for length in lengths]
            
            oldlength = 0
            
            for id, length in enumerate(lengths):
                if oldlength <= begin <= length:
                    beginid = id
                    beginpos = (begin - oldlength) / (length - oldlength)
                if oldlength <= end <= length:
                    endid = id
                    endpos = (end - oldlength) / (length - oldlength)
                
                oldlength = length
            
            beginpoint = CLine(points[beginid], points[beginid+1]).Scale(beginpos).GetEnd().GetPos()
            endpoint = CLine(points[endid], points[endid+1]).Scale(endpos).GetEnd().GetPos()
            
            points = [beginpoint] + points[beginid + 1 : endid + 1] + [endpoint]
        
        oldpoint = None
        
        for point in points:
            if oldpoint is not None:
                context.GetCanvas().DrawLine(oldpoint, point, color, line_width = width, line_style = style)
            oldpoint = point
