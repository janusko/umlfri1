import sqlite3
import Connection, Element, ConLabelInfo
from lib.config import config
from lib.Drawing.Context import CDrawingContext


class CSelection:
    '''Set of selected elements and connections'''
    def __init__(self):
        self.selected = set()

    def __AddSquare(self, index, x, y, posx, posy, element):
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
        element.GetSquares().append(((-posx, -posy), (x, y), (x1 - x, y1 - y)))
        
    def GetSelected(self):
        selected = tuple(self.selected)
        for i in selected:
            if i in self.selected:
                yield i

    def GetSelectedElements(self, nolabels = False):
        for i in self.selected:
            if nolabels:
                if isinstance(i, Element.CElement):
                    yield i
            else:
                if isinstance(i, (Element.CElement, ConLabelInfo.CConLabelInfo)):
                    yield i

    def GetSelectedConnections(self):
        for i in self.selected:
            if isinstance(i, Connection.CConnection):
                yield i

    def SelectedCount(self):
        return len(self.selected)

    def AddToSelection(self, element):
        self.selected.add(element)
        element.Select()

    def RemoveFromSelection(self, element):
        self.selected.remove(element)
        element.Deselect()

    def DeselectAll(self):
        for e in self.selected:
            e.Deselect()
        self.selected = set()

    def SelectAll(self):
        for e in self.elements:
            self.selected.add(e)
            e.Select()

        for c in self.connections:
            self.selected.add(c)
            c.Select()

    def IsSelected(self, selObj):
        '''
        Checks if selObj is selected.
        @param selObj: CSelectableObject
        @return: bool
        '''
        for i in self.selected:
            if i is selObj:
                return True

        return False

    def PaintSelection(self, canvas, selObj, delta = (0, 0)):
        '''
        Draws selection for selObj, if selObj is located in self.selected.

        @param canvas:
        @param selObj: CSelectableObject
        @param delta:
        '''
        if self.IsSelected(selObj):

            if isinstance(selObj, Element.CElement):
                x, y = selObj.GetPosition()
                context = CDrawingContext(selObj, (x + delta[0], y + delta[1]))
                rx, ry = selObj.GetObject().GetType().GetResizable(context)

                minsize = selObj.GetMinimalSize()

                # calculate actual size from delta size, if loaded older version of project (1.1.0)
                if selObj.hasDeltaSize:
                    selObj.hasDeltaSize = False
                    selObj.actualSize = ( minsize[0] + selObj.actualSize[0], minsize[1] + selObj.actualSize[1] )

                w, h = selObj.GetSize()
                wasSmall = False
                if w < minsize[0]:
                    w = minsize[0]
                    wasSmall = True
                if h < minsize[1]:
                    h = minsize[1]
                    wasSmall = True
                if wasSmall:
                    selObj.SetSize((w, h))

                selObj.squares = []

                if rx and ry:
                    self.__AddSquare(0, x       , y       ,  1,  1, selObj)
                    self.__AddSquare(2, x + w   , y       , -1,  1, selObj)
                    self.__AddSquare(5, x       , y + h   ,  1, -1, selObj)
                    self.__AddSquare(7, x + w   , y + h   , -1, -1, selObj)
                if ry:
                    self.__AddSquare(1, x + w//2, y       ,  0,  1, selObj)
                    self.__AddSquare(6, x + w//2, y + h   ,  0, -1, selObj)
                if rx:
                    self.__AddSquare(3, x       , y + h//2,  1,  0, selObj)
                    self.__AddSquare(4, x + w   , y + h//2, -1,  0, selObj)

                dx, dy = delta
                for i in selObj.GetSquares():
                    canvas.DrawRectangle((i[1][0] + dx, i[1][1] + dy), i[2], None, config['/Styles/Selection/PointsColor'])

                canvas.DrawRectangle((x + dx, y + dy), (w, h), fg = config['/Styles/Selection/RectangleColor'], line_width = config['/Styles/Selection/RectangleWidth'])
            elif isinstance(selObj, Connection.CConnection):
                size = config['/Styles/Selection/PointsSize']
                color = config['/Styles/Selection/PointsColor']
                dx, dy = delta
                for index, i in enumerate(selObj.GetPoints()):
                    canvas.DrawRectangle((i[0] + dx - size//2, i[1] + dy - size//2), (size, size), color)
                for label in selObj.labels.values():
                    canvas.DrawRectangle(label.GetPosition(), label.GetSize(), color)
