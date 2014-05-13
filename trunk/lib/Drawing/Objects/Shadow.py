from SimpleContainer import CSimpleContainer
from lib.Exceptions.UserException import *
from lib.datatypes import CColor

class CShadow(CSimpleContainer):
    types = {
        'padding': int,
        'color': CColor
    }
    def __init__(self, padding, color):
        CSimpleContainer.__init__(self)
        self.padding = padding
        self.color = color

    def Paint(self, context, canvas):
        if context.GetShadowColor() is not None:
            raise DrawingError("ShadowInShadow")
        size = context.ComputeSize(self)
        pos = context.GetPos()
        color, = self.GetVariables(context, 'color')
        
        context.Push()
        context.SetShadowColor(color)
        context.Move((pos[0] + self.padding, pos[1] + self.padding))
        CSimpleContainer.Paint(self, context, canvas)
        context.Pop()
        
        CSimpleContainer.Paint(self, context, canvas)
