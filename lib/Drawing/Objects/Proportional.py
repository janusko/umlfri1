from Align import CAlign
from lib.Exceptions.UserException import *

class CProportional(CAlign):
    types = {
        'ratio': float,
        'align': str,
        'size': str
    }
    def __init__(self, ratio, align = (None, None), size = "maximal"):
        CAlign.__init__(self, align)
        
        self.strratio = ratio
        self.ratio = ratio
        self.size = size

    def ComputeChildSize(self, context):
        w, h = context.ComputeSize(self.GetChild())
        ch = int(w / self.ratio)
        cw = int(h * self.ratio)
        if self.size == "minimal":
            if ch < h:
                h = ch
            if cw < w:
                w = cw
        else:
            if ch > h:
                h = ch
            if cw > w:
                w = cw
        return (w, h)

    def ComputeSize(self, context):
        return self.ComputeChildSize(context)
    
    def GetResizable(self, context):
        rx, ry = CAlign.GetResizable(self, context)
        resizable = rx or ry
        return resizable, resizable
