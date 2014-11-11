from lib.config import config
from lib.Drawing import CConnection
from CacheableObject import CCacheableObject
from Context import CDrawingContext

class CVisibleObject(CCacheableObject):
    '''
    Ancestor for CElement and CConLabel    
    '''
    
    def __init__(self):
        '''
        Common initialization of the visible object
        '''
        self.position = (0,0)
        # tuple for actual size of element
        # delta size-based computing of size
        self.actualSize = (0,0)
        CCacheableObject.__init__(self)

    def AreYouAtPosition(self, pos):
        x, y = pos
        width, height = self.GetSize()
        return self.position[0] <= x <= self.position[0] + width and \
            self.position[1] <= y <= self.position[1] + height
    
    def AreYouInRange(self, topleft, bottomright, all = False):
        (x1, y1), (x2, y2) = topleft, bottomright
        width, height = self.GetSize()
        
        if all:
            return (x1 <= self.position[0] <= self.position[0] + width <= x2) and (y1 <= self.position[1] <= self.position[1] + height <= y2)
        else:
            return ((x1 <= self.position[0] <= x2) and (y1 <= self.position[1] <= y2)) or \
                   ((x1 <= self.position[0] + width <= x2) and (y1 <= self.position[1] + height <= y2)) or \
                   ((self.position[0] <= x1 <= self.position[0] + width) and (self.position[1] <= y1 <= self.position[1] + height))
    
    def GetObject(self):
        return self.object
    
    def GetPosition(self, *ignored):
        return self.position
        
    def GetCenter(self):
        w, h = self.GetSize()
        return w / 2 + self.position[0], h / 2 + self.position[1]

    def SetSize(self, size):
        self.actualSize = size

    def GetSize(self):
        return self.actualSize
        
    def GetMinimalSize(self):
        w, h = self.object.GetSize(CDrawingContext(self, (0, 0)))
        return w, h
        
    def GetSquare(self):
        x, y = self.GetPosition()
        w, h = self.GetSize()
        return ((x, y), (x + w, y + h))
    
    def SetPosition(self, pos, *ignored):
        self.position = tuple(pos)
        
    def GetDiagram(self):
        return self.diagram()
        

