from VisualObject import CVisualObject

from lib.datatypes import CColor

class CConnectionLine(CVisualObject):
    types = {
        'color': CColor,
        'style': str,
        'width': int
    }
    def __init__(self, color = CColor('black'), style = 'solid', width = 1):
        CVisualObject.__init__(self)
        
        self.color = color
        self.style = style
        self.width = width

    def ComputeSize(self, context):
        return 0, 0

    def Paint(self, context):
        color, style, width = self.GetVariables(context, 'color', 'style', 'width')
        
        if context.GetShadowColor() is not None:
            color = context.GetShadowColor()
        
        start = None
        
        for end in context.GetPoints():
            if start is not None:
                context.GetCanvas().DrawLine(start, end, color, line_width = width, line_style = style)
            start = end
