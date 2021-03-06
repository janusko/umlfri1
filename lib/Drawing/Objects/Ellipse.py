from SimpleContainer import CSimpleContainer
from lib.datatypes import CColor

class CEllipse(CSimpleContainer):
    types = {
        'fill': CColor,
        'border': CColor,
        'borderwidth': int
    }
    def __init__(self, fill = None, border = CColor("white"), borderwidth = 1):
        CSimpleContainer.__init__(self)
        self.fill = fill
        self.border = border
        
        self.borderwidth = borderwidth
    
    def GetResizable(self, context):
        return True, True

    def Paint(self, context, canvas):
        size = context.ComputeSize(self)
        shadowcolor = context.GetShadowColor()
        if shadowcolor is None:
            border, fill = self.GetVariables(context, 'border', 'fill')
        else:
            border, fill = None, shadowcolor
        
        canvas.DrawArc(context.GetPos(), context.GetSize(), (0, 360), border, fill)
        
        if shadowcolor:
            return
        
        for i in self.childs:
            i.Paint(context, canvas)
