from lib.Base import CBaseObject

class CDrawingContext(CBaseObject):
    def __init__(self, canvas, element, pos, size = (None, None)):
        self.canvas = canvas
        self.element = element
        self.pos = pos
        self.size = size
        self.variables = {}
        self.defaults = {}
        self.stack = []
        self.shadowcolor = None
        self.line = 0
    
    def Push(self):
        self.stack.append((self.pos, self.size, self.variables.copy(), self.stack, self.shadowcolor, self.line, self.defaults.copy()))
    
    def Pop(self):
        self.pos, self.size, self.variables, self.stack, self.shadowcolor, self.line, self.defaults = self.stack.pop()

    def SetPosition(self, position):
        """
        Set position to the center of the DrawingContext
        @param position: actual position of DrawingContext
        """
        self.pos = position

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
        dx, dy = self.pos
        for x, y in self.element.GetPoints():
            yield x + dx, y + dy
    
    def GetLoopPath(self):
        return tuple(i[5] for i in self.stack) + (self.line, )
    
    def GetMetamodel(self):
        return self.element.GetObject().GetType().GetMetamodel()
    
    def SetDefault(self, name, value):
        self.defaults[name] = value
    
    def GetDefault(self, name):
        return self.defaults.get(name)
