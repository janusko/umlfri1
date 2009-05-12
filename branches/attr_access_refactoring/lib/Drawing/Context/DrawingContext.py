class CDrawingContext(object):
    def __init__(self, canvas, element, pos, size = (None, None)):
        self.canvas = canvas
        self.element = element
        self.pos = pos
        self.size = size
        self.variables = {}
        self.stack = []
        self.shadowcolor = None
        self.line = 0
    
    def Push(self):
        self.stack.append((self.pos, self.size, self.variables.copy(), self.stack, self.shadowcolor, self.line))
    
    def Pop(self):
        self.pos, self.size, self.variables, self.stack, self.shadowcolor, self.line = self.stack.pop()
    
    def ComputeSize(self, object):
        size = self.size
        if None in size:
            w, h = object.GetSize(self)
            if size[0] is None:
                size = w, size[1]
            if size[1] is None:
                size = size[0], h
        return size
    
    def GetSize(self):
        return self.size
    
    def GetCachedSize(self, object):
        return self.element.GetCachedSize(self, object)
    
    def GetPos(self):
        return self.pos
    
    def GetCanvas(self):
        return self.canvas
    
    def GetShadowColor(self):
        return self.shadowcolor
    
    def GetLine(self):
        return self.line
    
    def GetVariable(self, varname):
        return self.variables[varname]
    
    def GetVariables(self):
        return self.variables
    
    def GetProjectNode(self):
        obj = self.element.GetObject()
        if hasattr(obj, 'GetNode'):
            return obj.GetNode()
        else:
            return None
    
    def GetDomainObject(self):
        return self.element.GetObject().GetDomainObject()
    
    __getitem__ = GetVariable
    
    def Resize(self, newsize):
        self.size = newsize
    
    def CacheSize(self, object, size):
        return self.element.CacheSize(self, object, size)
    
    def Move(self, newpos):
        self.pos = newpos
    
    def SetVariables(self, vars):
        self.variables.update(vars)
    
    def SetLine(self, line):
        self.line = line
    
    def SetShadowColor(self, color):
        self.shadowcolor = color
    
    def GetPoints(self):
        return self.element.GetPoints(self.canvas)
    
    def GetLoopPath(self):
        return tuple(i[5] for i in self.stack) + (self.line, )