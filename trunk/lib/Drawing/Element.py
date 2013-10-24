from lib.config import config
from Connection import CConnection
from Context import CDrawingContext
from VisibleObject import CVisibleObject
import weakref

class CElement(CVisibleObject):
    def __init__(self, diagram, obj, isLoad = False):
        CVisibleObject.__init__(self)
        self.isLoad = isLoad
        self.object = obj
        self.squares = []
        self.diagram = weakref.ref(diagram)
        self.diagram().AddElement(self)
        self.object.AddAppears(diagram)
        self.__AddExistingConnections()
    
    def GetDiagram(self):
        return self.diagram()
    
    def __AddExistingConnections(self):
        if not self.isLoad:
            for i in self.object.GetConnections():
                if i.GetSource() is not self.object:
                    if self.diagram().HasElementObject(i.GetSource()) is not None:
                        CConnection(self.diagram(),i,self.diagram().HasElementObject(i.GetSource()),self)
                elif i.GetDestination() is not self.object:
                    if self.diagram().HasElementObject(i.GetDestination()) is not None:
                        CConnection(self.diagram(),i,self,self.diagram().HasElementObject(i.GetDestination()))
                    
    def __AddSquare(self, index, x, y, posx, posy):
        size = config['/Styles/Selection/PointsSize']
        if posx == 0:
            x = x - size // 2
            x1 = x + size
        else:
            x1 = x + posx * size
        if posy == 0:
            y = y - size // 2
            y1 = y + size
        else:
            y1 = y + posy * size
        if x1 < x:
            x1, x = x, x1
        if y1 < y:
            y1, y = y, y1
        self.squares.append(((-posx, -posy), (x, y), (x1 - x, y1 - y)))
    
    def Deselect(self):
        CVisibleObject.Deselect(self)
        self.squares = []

    def Paint(self, canvas, delta = (0, 0)):
        x, y = self.position
        context = CDrawingContext(canvas, self, (x + delta[0], y + delta[1]))
        
        rx, ry = self.object.GetType().GetResizable(context)
        
        #self.deltaSize = (
        #    self.deltaSize[0] if rx else 0,
        #    self.deltaSize[1] if ry else 0,
        #)

        minsize = self.GetMinimalSize(canvas)
        w, h = self.GetSize()
        wasSmall = False
        if w < minsize[0]:
            w = minsize[0]
            wasSmall = True
        if h < minsize[1]:
            h = minsize[1]
            wasSmall = True
        if wasSmall:
            self.SetSize((w, h))
        
        context.Resize((w, h))
        self.object.Paint(context)
        if self.selected:
            
            self.squares = []
            
            if rx and ry:
                self.__AddSquare(0, x       , y       ,  1,  1)
                self.__AddSquare(2, x + w   , y       , -1,  1)
                self.__AddSquare(5, x       , y + h   ,  1, -1)
                self.__AddSquare(7, x + w   , y + h   , -1, -1)
            if ry:
                self.__AddSquare(1, x + w//2, y       ,  0,  1)
                self.__AddSquare(6, x + w//2, y + h   ,  0, -1)
            if rx:
                self.__AddSquare(3, x       , y + h//2,  1,  0)
                self.__AddSquare(4, x + w   , y + h//2, -1,  0)
            
            dx, dy = delta
            for i in self.squares:
                canvas.DrawRectangle((i[1][0] + dx, i[1][1] + dy), i[2], None, config['/Styles/Selection/PointsColor'])
            
            canvas.DrawRectangle((x + dx, y + dy), (w, h), fg = config['/Styles/Selection/RectangleColor'], line_width = config['/Styles/Selection/RectangleWidth'])

    def GetConnections(self):
        for c1 in self.GetObject().GetConnections(): #ConnectionObject
            for c2 in self.diagram().GetConnections(): # Connection
                if c2.GetObject() is c1:
                    yield c2

    
    def GetSquareAtPosition(self, pos):
        x, y = pos
        for sq in self.squares:
            sqbx = sq[1][0]
            sqby = sq[1][1]
            sqex = sqbx + sq[2][0]
            sqey = sqby + sq[2][1]
            if (x >= sqbx and x <= sqex and y >= sqby and y <= sqey):
                return sq[0]
    
    def Resize(self, delta, selSquareIdx):
        '''
        Updates actual size according to delta size and if necessary changes position
        '''
        resRect = self.GetResizedRect(delta, selSquareIdx)
        self.position = resRect[0]
        self.actualSize = (max(0, resRect[1][0]), max(0, resRect[1][1]))

    def GetResizedRect(self, delta, mult):
        # updates position and checks if delta size is not greater than actual size
        pos = list(self.GetPosition())
        size = list(self.actualSize)
        
        for i in (0, 1):
            if mult[i] < 0:
                if delta[i] > size[i]:
                    pos[i] += size[i]
                    size[i] = 0
                else:
                    pos[i] += delta[i]
                    size[i] -= delta[i]
            else:
                size[i] = max(0, size[i] + mult[i] * delta[i])

        return pos, size
        
    def CopyFromElement(self, element):
        self.actualSize = element.actualSize
        self.position = element.position
    
    def GetObject(self):
        return self.object
