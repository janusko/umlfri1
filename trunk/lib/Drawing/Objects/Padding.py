from SimpleContainer import CSimpleContainer

class CPadding(CSimpleContainer):
    types = {
        'padding': int,
        'left': int,
        'right': int,
        'top': int,
        'bottom': int,
    }
    def __init__(self, padding = None, left = None, right = None, top = None, bottom = None):
        CSimpleContainer.__init__(self)
        
        if padding is not None:
            self.left = padding
            self.right = padding
            self.top = padding
            self.bottom = padding
        else:
            self.left = 0 if left is None else left
            self.right = 0 if right is None else right
            self.top = 0 if top is None else top
            self.bottom = 0 if bottom is None else bottom

    def ComputeSize(self, context):
        w, h = CSimpleContainer.ComputeSize(self, context)
        return (w + self.left + self.right, h + self.top + self.bottom)

    def Paint(self, context):
        size = context.ComputeSize(self)
        pos = context.GetPos()
        
        context.Push()
        context.Move((pos[0]+self.left, pos[1]+self.top))
        context.Resize((size[0] - self.left - self.right, size[1] - self.top - self.bottom))
        CSimpleContainer.Paint(self, context)
        context.Pop()
