from SimpleContainer import CSimpleContainer
from lib.Exceptions.UserException import *

class CAlign(CSimpleContainer):
    types = {
        'align': str
    }
    def __init__(self, align):
        CSimpleContainer.__init__(self)
        self.alignx = None
        self.aligny = None
        if isinstance(align, tuple):
            self.alignx, self.aligny = align
        else:
            align = align.split()
            if len(align) > 2:
                raise XMLError("Align", "align")
            if align == ['center', 'center']:
                self.alignx, self.aligny = align
            elif 'center' in align:
                if align[0] == 'center':
                    self.alignx = 'center'
                    del align[0]
                else:
                    self.aligny = 'center'
                    del align[1]
            for i in align:
                if i in ('left', 'right'):
                    self.alignx = i
                elif i in ('bottom', 'top'):
                    self.aligny = i
                elif i == 'middle':
                    self.aligny = 'center'
    
    def GetResizable(self, context):
        if self.alignx is None or self.aligny is None:
            rx, ry = CSimpleContainer.GetResizable(self, context)
        else:
            rx, ry = False, False
        return self.alignx is not None or rx, self.aligny is not None or ry
    
    def ComputeChildSize(self, context):
        return self.GetChild().GetSize(context)

    def Paint(self, context, canvas):
        x, y = context.GetPos()
        we, he = context.GetSize()
        w, h = context.ComputeSize(self)
        wc, hc = self.ComputeChildSize(context)
        alignx, aligny = self.GetVariables(context, 'alignx', 'aligny')
        
        if we is not None:
            if self.alignx is None:
                wc = w
            elif alignx == "center":
                x += (w - wc)/2
            elif alignx == "right":
                x += w - wc
        if he is not None:
            if self.aligny is None:
                hc = h
            elif aligny == "center":
                y += (h - hc)/2
            elif aligny == "bottom":
                y += h - hc
        
        context.Push()
        context.Move((x, y))
        context.Resize((wc, hc))
        CSimpleContainer.Paint(self, context, canvas)
        context.Pop()
