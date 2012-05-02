from SimpleContainer import CSimpleContainer
from lib.Exceptions.UserException import *

class CSizer(CSimpleContainer):
    types = {
        'minwidth': int,
        'minheight': int,
        'maxwidth': int,
        'maxheight': int,
        'width': int,
        'height': int
    }
    def __init__(self, minwidth = None, minheight = None, maxwidth = None, maxheight = None, width = None, height = None):
        CSimpleContainer.__init__(self)
        
        if (minwidth is not None or maxwidth is not None) and width is not None:
            raise XMLError("sizer", "width")
        if (minheight is not None or maxheight is not None) and height is not None:
            raise XMLError("sizer", "height")
        
        if minwidth is None:
            self.minwidth = None
        else:
            self.minwidth = minwidth
        if maxwidth is None:
            self.maxwidth = None
        else:
            self.maxwidth = maxwidth
        if minheight is None:
            self.minheight = None
        else:
            self.minheight = minheight
        if maxheight is None:
            self.maxheight = None
        else:
            self.maxheight = maxheight
        if width is None:
            self.width = None
        else:
            self.width = width
        if height is None:
            self.height = None
        else:
            self.height = height
    
    def GetResizable(self):
        if self.width is None or self.height is None:
            rx, ry = CSimpleContainer.GetResizable(self)
        return self.width is None and rx, self.height is None and ry

    def ComputeSize(self, context):
        w, h = CSimpleContainer.ComputeSize(self, context)
        
        if self.height is not None:
            h = self.height
        elif self.minheight is not None and self.minheight > h:
            h = self.minheight
        elif self.maxheight is not None and self.maxheight < h:
            h = self.maxheight
        
        if self.width is not None:
            w = self.width
        elif self.minwidth is not None and self.minwidth > w:
            w = self.minwidth
        elif self.maxwidth is not None and self.maxwidth < w:
            w = self.maxwidth
        
        return (w, h)

    def Paint(self, context):
        size = context.ComputeSize(self)
        
        context.Push()
        context.Resize(size)
        CSimpleContainer.Paint(self, context)
        context.Pop()
