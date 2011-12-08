from lib.Exceptions.UserException import *
from lib.Exceptions.UMLException import UMLException
from lib.config import config
import Connection, Element, ConLabelInfo
from lib.Math2D import CRectangle
from lib.Math2D import CPoint
from lib.Domains import CDomainObject, CDomainFactory
from lib.consts import DEFAULT_IDENTITY
from lib.Base import CBaseObject
from lib.Drawing.Grid import CGrid
import weakref
    
class CDiagram(CBaseObject):
    def __init__(self, type, name = None): #  name = "untitled"
        self.elements = []
        self.connections = []
        self.selected = set()
        self.type = type
        if type is not None:
            self.domainobject = CDomainObject(type.GetDomain())
        else:
            self.domainobject = CDomainObject(CDomainFactory.startPageDomain)
        self.size = None
        self.viewport = ((0, 0), (0, 0))
        self.scrollingPos = [0, 0]                  #position on diagram (needed for scrollBars)
        if name is None:
            self.SetName(self.type.GenerateName())
        else:
            self.SetName(name)
        self.revision = 0
        self.grid = CGrid()
        
    def GetObject(self):
        return self
    
    def GetValue(self, name):
        return self.domainobject.GetValue(name)
        
    def GetDomainName(self, key=''):
        return self.domainobject.GetDomainName(key)
    
    def GetDomainType(self, key=''):
        return self.domainobject.GetType(key)
    
    def GetDomainObject(self):
        return self.domainobject
    
    def SetValue(self, key, value):
        self.domainobject.SetValue(key, value)
        self.revision += 1
        
    def AppendItem(self, key, value = None):
        self.domainobject.AppendItem(key, value)
        self.revision += 1
    
    def RemoveItem(self, key):
        self.domainobject.RemoveItem(key)
        self.revision += 1
    
    def GetSaveInfo(self):
        return self.domainobject.GetSaveInfo()
    
    def SetSaveInfo(self, value):
        return self.domainobject.SetSaveInfo(value)
    
    def HasVisualAttribute(self, key):
        return self.domainobject.HasVisualAttribute(key)
        
    def GetRevision(self):
        """
        Get revision of this object. Revision is incremented after each
        object state chage
        
        @return: Object revision
        @rtype:  integer
        """
        return self.revision
    
    def AddRevision(self):
        """
        Increase revision on external change (Like movement in project tree)
        """
        
        self.revision += 1
    
    def GetName(self):
        if self.type:
            return self.domainobject.GetValue(self.type.GetIdentity() or DEFAULT_IDENTITY)
        else:
            return self.name
        
    def SetName(self, value):
        if self.type:
            self.domainobject.SetValue(self.type.GetIdentity() or DEFAULT_IDENTITY if self.type else DEFAULT_IDENTITY, value)
        else:
            self.name = value
    
    def GetHScrollingPos(self):
        return self.scrollingPos[0]
    
    def GetVScrollingPos(self):
        return self.scrollingPos[1]
    
    def SetHScrollingPos(self, value):
        self.scrollingPos[0] = value
    
    def SetVScrollingPos(self, value):
        self.scrollingPos[1] = value
        
    def HasElementObject(self, object):
        for i in self.elements:
            if i.GetObject() is object:
                return i
        return None
    
    def GetElementZOrder(self, object):
        return self.elements.index(object)
    
    def GetConnection(self, conObject):
        for c in self.connections:
            if c.GetObject() is conObject:
                return c
        return None
    
    def HasConnection(self, conObject):
        for c in self.connections:
            if c.GetObject() is conObject:
                return True
        return False
    
    def GetElement(self, elObject):
        for e in self.elements:
            if e.GetObject() is elObject:
                return e
        return None
    
    def HasElement(self, elObject):
        for e in self.elements:
            if e.GetObject() is elObject:
                return True
        return False
    
    def GetType(self):
        return self.type
    
    def AddElement(self, element):
        self.size = None
        if element not in self.elements:
            if element.GetObject().GetType().GetId() not in self.type.GetElements():
                raise DrawingError("DiagramHaveNotThisElement", element)
            for i in self.elements:
                if i.GetObject() is element.GetObject():
                    raise DrawingError("ElementAlreadyExists", element)
            self.elements.append(element)
        else:
            raise DrawingError("ElementAlreadyExists", element)
     
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
            
    def AddConnection(self, connection):
        self.size = None
        if connection not in self.connections:
            self.connections.append(connection)
        else:
            raise DrawingError("ConnectionAlreadyExists")
            
    def SelectedCount(self):
        return len(self.selected)
    
    def AddToSelection(self, element):
        self.selected.add(element)
        element.Select()
    
    def AddRangeToSelection(self, canvas, topleft, rightbottom):
        for el in self.GetElementsInRange(canvas, topleft, rightbottom, False):
            self.selected.add(el)
            el.Select()
    
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
    
    def GetSelectSquare(self, canvas, includeConnections = False):
        x1, y1 = self.GetSize(canvas)
        x2, y2 = 0, 0
        
        for el in self.GetSelectedElements():
            x, y = el.GetPosition(canvas)
            w, h = el.GetSize(canvas)
            if x < x1:
                x1 = x
            if y < y1:
                y1 = y
            if x + w > x2:
                x2 = x + w
            if y + h > y2:
                y2 = y + h
        if includeConnections:
            for connection in self.GetSelectedConnections():
                for x, y in connection.GetMiddlePoints():
                    x1 = min(x, x1)
                    x2 = max(x, x2)
                    y1 = min(y, y1)
                    y2 = max(y, y2)
        return (int(x1), int(y1)), (int(x2 - x1), int(y2 - y1))
    
    def MoveSelection(self, delta, canvas = None):
        self.size = None
        deltax = max(delta[0], -min(el.GetSquare(canvas)[0][0] for el in self.GetSelectedElements()))
        deltay = max(delta[1], -min(el.GetSquare(canvas)[0][1] for el in self.GetSelectedElements()))
        movedCon = set()
        elements = set()
        if canvas is not None:
            for el in self.GetSelectedElements():
                if not isinstance(el, ConLabelInfo.CConLabelInfo):
                    pos1, pos2 = el.GetSquare(canvas)
                    zorder = self.elements.index(el)
                    for el2 in self.GetElementsInRange(canvas, pos1, pos2):
                        if not isinstance(el2, ConLabelInfo.CConLabelInfo):
                            if self.elements.index(el2) > zorder:
                                elements.add(el2)
        elements |= set(self.GetSelectedElements())
        condelta = self.grid.SnapPosition(delta) if self.grid.IsActive() \
            else delta
        for el in elements:
            x, y = el.GetPosition(canvas)
            self.MoveElement(el, (x + deltax, y + deltay), canvas)
            if not isinstance(el, ConLabelInfo.CConLabelInfo):
                for con in el.GetConnections():
                    if (con.GetSource() in elements) and (con.GetDestination() in elements):
                        if con not in movedCon:
                            con.MoveAll(condelta, canvas)
                            movedCon.add(con)
        if canvas is not None:
            for conn in self.connections:
                conn.ValidatePoints(canvas)
    
    def DeleteObject(self, object):
        self.size = None
        for o in self.elements:
            if o.GetObject() is object:
                for c in o.GetConnections():
                    self.ShiftDeleteConnection(c)
                self.DeleteItem(o)
                return
    
    def DeleteItem(self, item):
        self.size = None
        item.GetObject().RemoveAppears(self)
        if isinstance(item, ConLabelInfo.CConLabelInfo):
            self.DeleteConLabel(item)
        elif isinstance(item, Connection.CConnection):
            self.DeleteConnection(item)
        elif isinstance(item, Element.CElement):
            self.DeleteElement(item)
        else:
            raise DrawingError("UnknownItemClass")
        
        
    def DeleteElement(self, element):
        self.size = None
        if element in self.elements:
            deleted = []
            self.elements.remove(element)
            if element in self.selected:
                self.selected.remove(element)
            for con in self.connections:
                if (con.GetSource() is element) or \
                    (con.GetDestination() is element):
                    deleted.append(con)
            for con in deleted:
                self.DeleteConnection(con)
        else:
            raise DrawingError("ElementDoesNotExists")
        
    def DeleteConLabel(self,conlabel):
        self.size = None
        self.DeleteConnection(conlabel.GetConnection())
        if conlabel in self.selected:
            self.selected.remove(conlabel)
            
    def ShiftDeleteConLabel(self,conlabel):
        self.size = None
        self.ShiftDeleteConnection(conlabel.GetConnection())
        if conlabel in self.selected:
            self.selected.remove(conlabel)
    
    def DeleteConnection(self, connection):
        self.size = None
        if connection in self.connections:
            self.connections.remove(connection)
            if connection in self.selected:
                self.selected.remove(connection)
        else:
            raise DrawingError("ConnectionDoesNotExists")
    
    def DeleteConnectionObject(self, object):
        for i in self.connections:
            if i.GetObject() is object:
                self.connections.remove(i)
                return
    
    def ShiftDeleteConnection(self, connection):
        self.size = None
        if connection in self.connections:
            obj = connection.GetObject()
            for a in obj.GetAppears():
                a.DeleteConnectionObject(obj)
                
            obj.GetSource().RemoveConnection(obj)
            if obj.GetSource() is not obj.GetDestination():
                obj.GetDestination().RemoveConnection(obj)
            #self.connections.remove(connection)
            if connection in self.selected:
                self.selected.remove(connection)
        else:
            raise DrawingError("ConnectionDoesNotExists")
    
    def GetSize(self, canvas):
        if self.size is not None:
            return self.size
        else:
            result = (0, 0)
            for connection in self.connections:
                for point in connection.GetMiddlePoints():
                    result = tuple(max(x) for x in zip(result, point))
            for element in self.elements:
                    point = tuple(sum(x) for x in zip(element.GetPosition(canvas), element.GetSize(canvas)))
                    result = tuple(max(x) for x in zip(result, point))
            page = (config['/Page/Width'], config['/Page/Height'])
            result = (page[0] * (result[0]//page[0] + 1), page[1] * (result[1]//page[1] + 1))
            self.size = result
        return result

        
    def GetElementAtPosition(self, canvas, pos):
        for c in self.connections:
            r = c.WhatPartOfYouIsAtPosition(canvas, pos)
            if isinstance(r, (int, long)):
                return c
            elif r is not None:
                return r
                
        for e in self.elements[::-1]:
            if e.AreYouAtPosition(canvas, pos):
                return e
            
        return None
    
    def GetElementsInRange(self, canvas, topleft, bottomright, includeall = True):
        for e in self.elements:
            if e.AreYouInRange(canvas, topleft, bottomright, includeall):
                yield e
    
    def SetViewPort(self, view):
        self.viewport = view
        
    def GetViewPort(self):
        return self.viewport

    #view = ((x, y), (w, h)
    def Paint(self, canvas):
        # TODO
        # optimize: multiple call for one update event:
        #   double calling on click-to-select-element

        ((x, y), (w, h)) = self.viewport
        canvas.Clear()
        self.grid.Paint(canvas, self.viewport)
        var = set([])
        for e in self.elements:#here is created a set of layer values
            var.add(int(e.GetObject().GetType().GetOptions().get('Layer', 0)))
        var=list(var)
        var.sort()#sorted list of layer values
        num=0
        for k in var:
            for e in self.elements:#elements are ordered depending on their layer (if they have one or their layer is set to default value)
                if int(e.GetObject().GetType().GetOptions().get('Layer',0))==k:
                    if not isinstance(e, ConLabelInfo.CConLabelInfo):
                        selectedIdx = self.elements.index(e)
                        del self.elements[selectedIdx]
                        self.elements.insert(num, e)
                        num+=1
        for e in self.elements:
            ((ex1, ey1), (ex2, ey2)) = e.GetSquare(canvas)
            if not (ex2 < x or x + w < ex1 or ey2 < y or y + w < ey1):
                e.Paint(canvas, delta = (-x, -y))
        for c in self.connections:
            ((ex1, ey1), (ex2, ey2)) = c.GetSquare(canvas)
            if not (ex2 < x or x + w < ex1 or ey2 < y or y + w < ey1):
                c.Paint(canvas, delta = (-x, -y))
            
    def PaintFull(self, canvas):
        """Paints the whole diagram. Used
        for exporting.
        """
        canvas.Clear()
        for e in self.elements:
            e.Paint(canvas)
        for c in self.connections:
            c.Paint(canvas)
        
    def PaintSelected(self, canvas):
        """Paints _only_ selected items (elements + connections)
        as if they were deselected. Used for pixbuf copying.
        """
        canvas.Clear()
        old_selected =  self.selected
        self.DeselectAll()
        setElements = set(e for e in old_selected if isinstance(e, Element.CElement))
        setConnections = set(e for e in old_selected if isinstance(e, Element.CConnection))
        for e in self.elements:
            if e in setElements:
                e.Paint(canvas)
                self.AddToSelection(e)
        for e in self.connections:
            if e in setConnections:
                e.Paint(canvas)
                self.AddToSelection(e)
 
    def GetElements(self):
        for e in self.elements:
            yield e
    
    def GetConnections(self):
        for c in self.connections:
            yield c

    def Assign(self, cprojNode):
        self.node = weakref.ref(cprojNode)
    
    def GetNode(self):
        return self.node()
    
    def ShiftElementsToTop(self):
        for selectedElement in self.GetSelectedElements():
            if not isinstance(selectedElement, ConLabelInfo.CConLabelInfo):
                selectedIdx = self.elements.index(selectedElement)
                del self.elements[selectedIdx]
                self.elements.append(selectedElement) 

    def ShiftElementsToBottom(self):
        for selectedElement in self.GetSelectedElements():
            if not isinstance(selectedElement, ConLabelInfo.CConLabelInfo):
                selectedIdx = self.elements.index(selectedElement)
                del self.elements[selectedIdx]
                self.elements.insert(0, selectedElement)

    def ShiftElementsForward(self, canvas):
        for selectedElement in self.GetSelectedElements():
            if not isinstance(selectedElement, ConLabelInfo.CConLabelInfo):
                selectedIdx = self.elements.index(selectedElement)
                selSq = selectedElement.GetSquare(canvas)
                selRect = CRectangle(CPoint(selSq[0]), CPoint(selSq[1]))
                selectedShifted = False
                otherElementIdx = selectedIdx + 1
                while otherElementIdx < len(self.elements) and selectedShifted == False:
                    othSq = self.elements[otherElementIdx].GetSquare(canvas)
                    othRect = CRectangle(CPoint(othSq[0]), CPoint(othSq[1]))
                    prienik = selRect*othRect 
                    if len(prienik) > 0:
                        del self.elements[selectedIdx]
                        self.elements.insert(otherElementIdx, selectedElement)
                        selectedShifted = True
                    otherElementIdx += 1
                
    def ShiftElementsBack(self, canvas):
        for selectedElement in self.GetSelectedElements():
            if not isinstance(selectedElement, ConLabelInfo.CConLabelInfo):
                selectedIdx = self.elements.index(selectedElement)
                selSq = selectedElement.GetSquare(canvas)
                selRect = CRectangle(CPoint(selSq[0]), CPoint(selSq[1]))
                selectedShifted = False
                otherElementIdx = selectedIdx - 1
                while otherElementIdx >= 0 and selectedShifted == False:
                    othSq = self.elements[otherElementIdx].GetSquare(canvas)
                    othRect = CRectangle(CPoint(othSq[0]), CPoint(othSq[1]))
                    prienik = selRect*othRect
                    if len(prienik) > 0:
                        del self.elements[selectedIdx]
                        self.elements.insert(otherElementIdx, selectedElement)
                        selectedShifted = True
                    otherElementIdx -= 1
    
    def CutSelection(self, clipboard):
        if self.selected:
            clipboard.SetContent((el for el in self.selected if isinstance(el, Element.CElement)))
            for el in list(self.selected):
                if isinstance(el, Element.CElement):
                    self.DeleteElement(el)
    
    def CopySelection(self, clipboard):
        if self.selected:
            clipboard.SetContent((el for el in self.selected if isinstance(el, Element.CElement)))
    
    def PasteSelection(self, clipboard):
        pasted = set()
        for i in clipboard.GetContent():
            try:
                el = Element.CElement(self, i.GetObject())
            except UMLException, e:
                for el in pasted:
                    self.DeleteElement(el)
                raise
            self.AddToSelection(el)
            el.CopyFromElement(i)
            pasted.add(el)

    def GetExpSquare(self, canvas):
        #square for export, the minimal size is measured so the exported diagram has the same edges - looks better
        x_max, y_max,x_min, y_min,  = 0, 0,  101, 101
        for el in self.elements:
            posX, posY = el.GetPosition(canvas)
            w, h = el.GetSize(canvas)
            if posX + w > x_max:
                x_max = posX + w
            if posY + h > y_max:
                y_max = posY + h
            if posX < x_min:
                x_min = posX
            if posY < y_min:
                y_min = posY

        for connection in self.connections:
            for point in connection.GetMiddlePoints():
                posX, posY = point
                if posX > x_max:
                    x_max = posX
                if posY > y_max:
                    y_max = posY
                if posX < x_min:
                    x_min = posX
                if posY < y_min:
                    y_min = posY
        if x_min > 100 :
            x_min = 100
        if y_min > 100 :
            y_min = 100
        return x_max +x_min, y_max + y_min

    def GetSizeSquare(self, canvas):
        x_max, y_max,x_min, y_min,  = 0, 0,  9999, 9999
        for el in self.elements:
            posX, posY = el.GetPosition(canvas)
            w, h = el.GetSize(canvas)
            if posX + w > x_max:
                x_max = posX + w
            if posY + h > y_max:
                y_max = posY + h
            if posX < x_min:
                x_min = posX
            if posY < y_min:
                y_min = posY
        for connection in self.connections:
            for point in connection.GetMiddlePoints():
                posX, posY = point
                if posX > x_max:
                    x_max = posX
                if posY > y_max:
                    y_max = posY
                if posX < x_min:
                    x_min = posX
                if posY < y_min:
                    y_min = posY
                  
        return (int(x_min),int(y_min)),(int(x_max), int(y_max))

    def ApplyNewSettings(self):
        """
        Called each time settings change.
        """
        self.grid.UpdatePattern()

    def SnapPositionToGrid(self, pos):
        return self.grid.SnapPosition(pos)

    def MoveElement(self, element, pos, canvas):
        if not isinstance(element, ConLabelInfo.CConLabelInfo):
            self.grid.SnapElement(element, pos, canvas)
        else:
            element.SetPosition(pos, canvas)
    
    def MoveConnectionPoint(self, conn, pos, idx, canvas):
        self.grid.SnapConnection(conn, pos, idx, canvas)

    def AlignElementsXY(self, isHorizontal, isLowerBoundary,
            canvas, defaultElement=None): 
        """
        Aligns selected elements along specified axis and position.
        If position isn't set, elements will be aligned to their average
        position.
    
        @param isHorizontal: align horizontaly or verticaly
        @type isHorizontal: bool
        @param isLowerBoundary: align to lower or higher boundary
        @type isLowerBoundary: bool
        @param canvas: drawing canvas
        @type canvas: L{CCairoCanvas<lib.Drawing.Canvas.Cairo.CCairoCanvas>}
        @param defaultElement: Element to align to
        @type defaultElement: L{CElement<lib.Drawing.Element.CElement>}
        """
        xy = 1-int(bool(isHorizontal))
        elements = tuple(self.GetSelectedElements())
        if len(elements)<2: return
        if not defaultElement:
            fun = min if isLowerBoundary else max
            most = elements[0].GetPosition()[xy] + \
                (0 if isLowerBoundary else elements[0].GetSize(canvas)[xy])
            for e in elements:
                most = fun( most, e.GetPosition()[xy] + \
                    (0 if isLowerBoundary else e.GetSize(canvas)[xy]) )
        else: 
            most = defaultElement.GetPosition()[xy] + \
                (0 if isLowerBoundary else defaultElement.GetSize(canvas)[xy])
        for e in elements:
            pos = list(e.GetPosition())
            pos[xy] = most - \
                ( 0 if isLowerBoundary else e.GetSize(canvas)[xy] )
            self.MoveElement(e, pos, canvas)
    
    def AlignElementCentersXY(self, isHorizontal, canvas, defaultElement=None):
        """
        Aligns centers of selected elements to defaultElements center 
        along x or y axis.
        If defaultElement it's set, elements will be aligned to their average
        center position.
        
        @param isHorizontal: align horizontaly or verticaly
        @type xy: bool
        @param canvas: drawing canvas
        @type canvas: L{CCairoCanvas<lib.Drawing.Canvas.Cairo.CCairoCanvas>}
        @param defaultElement: Element to align to
        @type defaultElement: L{CElement<lib.Drawing.Element.CElement>}
        """
        xy = 1-int(bool(isHorizontal))
        elements = tuple(self.GetSelectedElements())
        if len(elements)<2: return
        if not defaultElement:
            avg = 0
            for e in elements:
                avg += e.GetCenter(canvas)[xy]
            position = avg/len(elements)
        else:
            position = defaultElement.GetCenter(canvas)[xy]
        for e in elements:
            pos = list(e.GetPosition())
            pos[xy] = position - e.GetSize(canvas)[xy]/2
            self.MoveElement(e, pos, canvas)

    def SpaceElementsEvenlyXY(self, isHorizontal, canvas):
        """
        Spaces selected elements evenly along x or y axis. 
        
        @param xy: space horizontaly or verticaly
        @type xy: bool
        @param canvas: drawing canvas
        @type canvas: L{CCairoCanvas<lib.Drawing.Canvas.Cairo.CCairoCanvas>}
        """
        xy = 1-int(bool(isHorizontal))
        elements = list(self.GetSelectedElements())
        if len(elements)<3: return
        elemtotal = 0
        for e in elements:
            elemtotal += e.GetSize(canvas)[xy]
        total = self.GetSelectSquare(canvas)[1][xy]
        spacing = (total - elemtotal)/(len(elements) - 1)
        elements.sort(lambda x, y: cmp(x.GetPosition()[xy],\
            y.GetPosition()[xy]))
        pos = [0, 0]
        pos[xy] = elements[0].GetPosition()[xy]
        for e in elements:
            pos[1-xy] = e.GetPosition()[1-xy]
            self.MoveElement(e, pos, canvas)
            pos[xy] += e.GetSize(canvas)[xy] + spacing

    def ResizeElementsEvenly(self, resizeByWidth, canvas, selectedElement=None):
        """
        Resize selected elements evenly to minimal or maximal size of selected
        elements or requested size.
        
        @param reziseByWidth: resize to maximum or minimum
        @type resizeByWidth: bool
        @param canvas: drawing canvas
        @type canvas: L{CCairoCanvas<lib.Drawing.Canvas.Cairo.CCairoCanvas>}
        @param size: requested size
        @type size: list
        """    

        xy = 1 - int(resizeByWidth)
        
        if selectedElement:
            selectedElementSize = selectedElement.GetSize(canvas)
        elements = tuple(self.GetSelectedElements())
        if len(elements)<2: return
        minSelElSize = selectedElement.GetMinimalSize(canvas)
        
        for e in elements:
            esize = list(e.GetSizeRelative())
            actualElementMinimalSize = e.GetMinimalSize(canvas)               
            if actualElementMinimalSize[xy] <= selectedElementSize[xy]:
                if selectedElementSize[xy] < e.GetSize(canvas)[xy]:
                    esize[xy] = selectedElementSize[xy] - minSelElSize[xy]
                    e.SetSizeRelative(esize)                    
                if selectedElementSize[xy] > e.GetSize(canvas)[xy]:
                    esize[xy] = selectedElementSize[xy] - actualElementMinimalSize[xy]
                    e.SetSizeRelative(esize)
            if actualElementMinimalSize[xy] > selectedElementSize[xy]:
                if selectedElementSize[xy] < e.GetSize(canvas)[xy]:
                    esize[xy] = 0                
                    e.SetSizeRelative(esize)
                if selectedElementSize[xy] > e.GetSize(canvas)[xy]:
                    esize[xy] = selectedElementSize[xy] - actualElementMinimalSize[xy]
                    e.SetSizeRelative(esize)
    
    def ResizeByMaximalElement(self, canvas):
        '''
        Resize all elements based on the size of the maximal element
        '''
        elements = tuple(self.GetSelectedElements())
        if len(elements)<2: return

        maxhight = 0
        maxwidth = 0
        size = 0
        for e in elements:
            if size < e.GetSize(canvas)[0] + e.GetSize(canvas)[1]:
                size = e.GetSize(canvas)[0] + e.GetSize(canvas)[1]
                maxhight = e.GetSize(canvas)[0]
                maxwidth = e.GetSize(canvas)[1]
                
        for e in elements:
            esize = list(e.GetSizeRelative())
            actualElementMinimalSize = e.GetMinimalSize(canvas)
            esize[0] = maxhight - actualElementMinimalSize[0]
            esize[1] = maxwidth - actualElementMinimalSize[1]
            e.SetSizeRelative(esize)
            
    def ResizeByMinimalElement(self, canvas):
        '''
        Resize all elements based on the size of the minimal element
        '''
        elements = tuple(self.GetSelectedElements())
        if len(elements)<2: return
        
        minhight = 99999
        minwidth = 99999
        size = minhight + minwidth
        for e in elements:
            if size > e.GetSize(canvas)[0] + e.GetSize(canvas)[1]:
                size = e.GetSize(canvas)[0] + e.GetSize(canvas)[1]
                minhight = e.GetSize(canvas)[0]
                minwidth = e.GetSize(canvas)[1]
                
        for e in elements:
            esize = list(e.GetSizeRelative())
            actualElementMinimalSize = e.GetMinimalSize(canvas)
            if minhight < actualElementMinimalSize[0]:
                esize[0] = 0
            if minhight >= actualElementMinimalSize[0]:
                esize[0] = minhight - actualElementMinimalSize[0]
            if minwidth < actualElementMinimalSize[1]:
                esize[0] = 0
            if minwidth >= actualElementMinimalSize[1]:
                esize[1] = minwidth - actualElementMinimalSize[1]
            e.SetSizeRelative(esize)
            
    def SnapElementsOnGrid(self, canvas):
        '''
        Snaps selected elements on grid. Grid doesn't have to be active.
        '''
        elements = list(self.GetSelectedElements())
        if len(elements)<1: return
        for e in elements:
            pos = e.GetPosition()
            self.grid.SnapElement(e, pos, canvas, True)
        
