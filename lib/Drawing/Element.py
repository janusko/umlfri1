from lib.Drawing.ElementLabelInfo import CElementLabelInfo
from lib.config import config
from Connection import CConnection
from Context import CDrawingContext
from VisibleObject import CVisibleObject
import weakref

class CElement(CVisibleObject):
    def __init__(self, diagram, obj, isLoad = False, hasDeltaSize = False):
        CVisibleObject.__init__(self)
        self.isLoad = isLoad
        self.hasDeltaSize = hasDeltaSize
        self.object = obj
        self.diagram = weakref.ref(diagram)
        self.diagram().AddElement(self)
        self.labels = dict((id, CElementLabelInfo(self, logicalLabel))
                           for id, logicalLabel in enumerate(self.object.GetType().GetLabels()))
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

    def Paint(self, canvas):
        x, y = self.position
        context = CDrawingContext(self, (x, y))

        rx, ry = self.object.GetType().GetResizable(context)

        minsize = self.GetMinimalSize()

        # calculate actual size from delta size, if loaded older version of project (1.1.0)
        if self.hasDeltaSize:
            self.hasDeltaSize = False
            self.actualSize = ( minsize[0] + self.actualSize[0], minsize[1] + self.actualSize[1] )

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
        self.object.Paint(context, canvas)

    def GetConnections(self):
        for c1 in self.GetObject().GetConnections(): #ConnectionObject
            for c2 in self.diagram().GetConnections(): # Connection
                if c2.GetObject() is c1:
                    yield c2

    def Resize(self, delta, selSquareIdx):
        '''
        Updates actual size according to delta size and if necessary changes position
        '''
        resRect = self.GetResizedRect(delta, selSquareIdx)
        minSize = self.GetMinimalSize()
        self.position = resRect[0]
        self.actualSize = (max(minSize[0], resRect[1][0]), max(minSize[1], resRect[1][1]))

    def GetResizedRect(self, delta, mult):
        # updates position and checks if delta size is not greater than actual size
        pos = list(self.GetPosition())
        size = list(self.actualSize)
        minSize = self.GetMinimalSize()

        for i in (0, 1):
            if mult[i] < 0:
                if delta[i] > size[i] - minSize[i]:
                    pos[i] += size[i] - minSize[i]
                    size[i] = minSize[i]
                else:
                    pos[i] += delta[i]
                    size[i] -= delta[i]
            else:
                size[i] = max(minSize[i], size[i] + mult[i] * delta[i])

        return pos, size

    def CopyFromElement(self, element):
        self.actualSize = element.actualSize
        self.position = element.position

    def GetObject(self):
        return self.object