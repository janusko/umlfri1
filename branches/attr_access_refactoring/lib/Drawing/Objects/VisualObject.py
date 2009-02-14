from lib.config import config
from lib.Drawing.Context import CParamEval

class CVisualObject:
    types = {}
    def __init__(self):
        self.parent = None
    
    def __GetAttrs(self, value, names):
        for name in names:
            value = getattr(value, name)
        return value
    
    def GetVariables(self, context, *names):
        for name in names:
            value = getattr(self, name)
            if isinstance(value, CParamEval):
                yield value(context)
            else:
                yield value
    
    def GetResizable(self):
        return False, False
    
    def ComputeSize(self, context):
        return 0, 0
    
    def GetSize(self, context):
        size = context.GetCachedSize(self)
        if size is not None:
            return size
        size = self.ComputeSize(context)
        return context.CacheSize(self, size)

    def GetParent(self):
        return self.parent

    def Paint(self, context):
        pass

    def SetParent(self, parent):
        self.parent = parent
