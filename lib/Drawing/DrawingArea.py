from lib.Base import CBaseObject
from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand

from lib.Elements import CElementObject
from lib.Connections import CConnectionObject
from lib.Drawing import CDiagram, CConnection, CElement, CConLabelInfo
from lib.Drawing.DrawingHelper import PositionToPhysical, PositionToLogical

from lib.Gui.common import CGuiObject

from lib.Exceptions.UserException import *

from lib.config import config
from lib.consts import BUFFER_SIZE, SCALE_MIN, SCALE_MAX, SCALE_INCREASE

import thread
import gobject

class CDrawingArea(CGuiObject):

    def __init__(self, app, diagram):
        CGuiObject.__init__(self, app)

        # CDiagram(None,_("Start page"))
        self.viewPort = ((0, 0), (0, 0))
        self.buffer_size = ((0, 0), BUFFER_SIZE)
        self.scale = 1.0
        self.diagram = diagram

        self.setResize = True

        self.keydragPosition = None

        self.dnd = None
        self.selElem = None
        self.selSq = None

        self.__NewConnection = None

        self.__toolboxItem = (None, None)

        self.dragForegroundColor = config['/Styles/Drag/RectangleColor']
        self.dragLineWidth = config['/Styles/Drag/RectangleWidth']

        self.cursor = None
        self.cursors = {
            None: None,
            'grab': 'grab.png',
            'grabbing': 'grabbing.png'
        }

    def GetCursor(self):
        """
        Returns current cursor.

        @return: Type of current cursor.
        @rtype: str
        """
        return self.cursor

    def GetCursorFile(self):
        """
        Returns filename of image for current cursor.

        @return: Filename of cursor image.
        @rtype: str
        """
        return self.cursors[self.GetCursor()]

    def GetViewPort(self):
        """
        Returns current view port.

        @return: Rectangle representing current view port. Two tuples (x, y), (width, height).
        @rtype: tuple
        """
        return self.viewPort

    def SetViewPort(self, viewPort):
        """
        Changes current view port.

        @param viewPort: Rectangle representing new view port. Two tuples (x, y), (width, height).
        @type viewPort: tuple

        @rtype: bool
        @return: True, if drawing area needs to be resized, False if not.
        """
        self.viewPort = viewPort

        return self.__UpdateDrawingBuffer(viewPort)

    def GetViewPortPos(self):
        """
        Returns view port position.

        @return: Position of the view port.
        @rtype : tuple
        """
        return self.viewPort[0]

    def SetViewPortPos(self, pos = (0, 0)):
        """
        Changes view port position.

        @param pos: New view port position
        @type pos: tuple
        """
        self.viewPort = pos, self.GetViewPortSize()

    def GetViewPortSize(self):
        """
        Returns view port size

        @return: Size of the view port
        @rtype : tuple
        """
        return self.viewPort[1]

    def SetViewPortSize(self, size):
        """
        Changes view port size.

        @param size: New size of the view port
        @type size: tuple
        """
        viewPort = (self.GetViewPortPos(), size)
        self.SetViewPort(viewPort)

    def GetDiagram(self):
        """
        Returns associated diagram.

        @return: Associated diagram
        @rtype:  L{Diagram<Diagram>}
        """
        return self.diagram

    def GetAbsolutePos(self, (posx, posy)):
        """
        Converts relative coordinates to absolute.

        Coordinates are relative to view port position.

        @param posx: X coordinate of position.
        @type posx: int

        @param posx: Y coordinate of position.
        @type posx: int

        @return: Coordinates in absolute scale.
        @rtype : tuple
        """
        return PositionToLogical((posx, posy), self.scale, self.GetViewPortPos())

    def GetRelativePos(self, (posx, posy)):
        """
        Converts absolute coordinates to relative.

        Coordinates are relative to view port position.

        @param posx: X coordinate of position.
        @type posx: int

        @param posx: Y coordinate of position.
        @type posx: int

        @return: Coordinates in relative scale.
        @rtype : tuple
        """
        return PositionToPhysical((posx, posy), self.scale, self.GetViewPortPos())

    def GetScale(self):
        """
        Returns drawing area scale (zoom).

        @return: Scale of drawing area.
        @rtype : float
        """
        return self.scale

    def SetScale(self, scale):
        """
        Changes scale of drawing area (zoom).

        @param scale: New scale of drawing area.
        @type scale: float
        """
        if (scale >= SCALE_MIN) and (scale <= SCALE_MAX):
            self.scale = scale
            # self.AdjustScrollBars()
            self.Paint()

    def IncScale(self, scale):
        """
        Increases or decreases scale (zoom) based on @scale.

        @param scale: Specifies, whether the scale is increased or decreased.
        @type scale: float
        """
        tmp_scale = (SCALE_INCREASE*((self.scale+0.00001)//SCALE_INCREASE))+scale
        if (tmp_scale+0.00001 >= SCALE_MIN) and (tmp_scale-0.00001 <= SCALE_MAX):
            self.scale = tmp_scale
            self.disablePaint = True
            self.CenterZoom(scale)
            # self.AdjustScrollBars()
            self.disablePaint = False
            self.Paint()

    def Paint(self, canvas, changed = True):
        """
        Paints diagram at canvas

        @param canvas: Canvas on which its being drawn
        @type  canvas: L{CCairoCanvas<lib.Drawing.Canvas.CairoCanvas.CCairoCanvas>}
        """

        canvas.SetScale(self.scale)

        if changed:
            self.diagram.Paint(canvas, self.buffer_size)

        if self.dnd == 'resize':
            self.__DrawResRect(canvas)
        if self.dnd == 'rect' and self.keydragPosition is None:
            self.__DrawDragRect(canvas)
        elif self.dnd == 'point':
            self.__DrawDragPoint(canvas)
        elif self.dnd == 'line':
            self.__DrawDragLine(canvas)
        # elif self.dnd == 'move':
        #     self.__DrawDragMove(pos)
        # elif self.dnd == 'selection':
        #     self.__DrawDragSel(pos)
        elif self.__NewConnection is not None:
            self.__DrawNewConnection(canvas)

    def DeleteSelectedObjects(self):
        for sel in self.diagram.GetSelected():
            if isinstance(sel, CConnection):
                index = sel.GetSelectedPoint()
                if index is not None and (sel.GetSource() != sel.GetDestination() or len(tuple(sel.GetMiddlePoints())) > 2):
                    sel.RemovePoint(index)
                    self.diagram.DeselectAll()
                    self.Paint()
                    return
        for sel in self.diagram.GetSelected():
            self.diagram.DeleteItem(sel)
        self.diagram.DeselectAll()
        self.emit('selected-item', list(self.diagram.GetSelected()),False)
        self.Paint()

    def ShiftElements(self, actionName):
        if (actionName == 'SendBack'):
            self.diagram.ShiftElementsBack()
        elif (actionName == 'BringForward'):
            self.diagram.ShiftElementsForward()
        elif (actionName == 'ToBottom'):
            self.diagram.ShiftElementsToBottom()
        elif (actionName == 'ToTop'):
            self.diagram.ShiftElementsToTop()
        self.Paint()

    def CopySelectedObjects(self):
        self.diagram.CopySelection(self.application.GetClipboard())

    def CutSelectedObjects(self):
        self.diagram.CutSelection(self.application.GetClipboard())
        self.Paint()
        self.emit('selected-item', list(self.diagram.GetSelected()),False)

    def PasteObjects(self):
        self.diagram.PasteSelection(self.application.GetClipboard())
        self.Paint()
        self.emit('selected-item', list(self.diagram.GetSelected()),False)

    def DuplicateSelectedObjects(self):
        cmd  = CDuplicateElementsCommand(tuple(self.diagram.GetSelectedElements()), self.diagram)
        self.application.GetCommands().Execute(cmd)
        self.Paint()

    def ShiftDeleteSelectedObjects(self):
        for sel in self.diagram.GetSelected():
            if isinstance(sel, CElement):
                self.emit('delete-element-from-all',sel.GetObject())
            elif isinstance(sel, CConLabelInfo):
                self.diagram.ShiftDeleteConLabel(sel)
            else:
                self.diagram.ShiftDeleteConnection(sel)
        self.Paint()

    def ChangeSourceTarget(self):
        self.Paint()

    def ChangeConnectionSourceTarget(self):
        for sel in self.diagram.GetSelected():
            if isinstance(sel, CConnection):
                sel.GetObject().ChangeConnection()
            project = self.application.GetProject()
            diagrams = project.GetDiagrams()
            for d in diagrams:
                for c in d.GetConnections():
                    if c.GetObject() == sel.GetObject():
                        c.ChangeConnection()
                        self.Paint()

    def Align(self, isHorizontal, isLowerBoundary,
            alignToSelectedElement=True):
        self.diagram.AlignElementsXY(isHorizontal, alignToSelectedElement, self.itemSel if alignToSelectedElement else None)
        self.Paint()

    def AlignCenter(self, isHorizontal, alignToSelectedElement = True):
        self.diagram.AlignElementCentersXY(isHorizontal, self.itemSel if alignToSelectedElement else None)
        self.Paint()

    def ResizeHeight(self):
        self.diagram.ResizeElementsEvenly(False, self.itemSel)
        self.Paint()

    def ResizeWidth(self):
        self.diagram.ResizeElementsEvenly(True, self.itemSel)
        self.Paint()

    def ResizeWidthAndHeight(self):
        self.diagram.ResizeElementsEvenly(True, self.itemSel)
        self.diagram.ResizeElementsEvenly(False, self.itemSel)
        self.Paint()

    def ResizeByMaximalElement(self):
        self.diagram.ResizeByMaximalElement()

    def ResizeByMinimalElement(self):
        self.diagram.ResizeByMinimalElement()
        self.Paint()

    def SnapSelected(self):
        self.diagram.SnapElementsOnGrid()
        self.Paint()

    def MakeSpacing(self, isHorizontal):
        self.diagram.SpaceElementsEvenlyXY(isHorizontal)
        self.Paint()

    def PaintSelected(self, canvas):
        self.diagram.PaintSelected(canvas)

    def __UpdateDrawingBuffer(self, viewport):
        posx, posy = viewport[0]
        sizx, sizy = viewport[1]

        ((bposx, bposy), (bsizx, bsizy)) = self.buffer_size
        (bposx, bposy) = PositionToPhysical((bposx, bposy))

        bufferResized = False

        # resize buffer rectangle, if we get out of its bounds
        if posx < bposx or bposx + bsizx < posx + sizx or \
           posy < bposy or bposy + bsizy < posy + sizy:

            bposx = posx + (sizx - bsizx)//2
            bposy = posy + (sizy - bsizy)//2

            (bposx, bposy) = PositionToLogical((bposx, bposy))

            self.buffer_size = ((bposx, bposy), (bsizx, bsizy))

            bufferResized = True

        return bufferResized

    def OnMouseMove(self, pos):
        """
        Callback for mouse move event (motion-notify-event)

        @param pos: Current mouse position.
        @type pos: tuple
        """
        pos = self.GetAbsolutePos(pos)

        if self.dnd == 'resize':
            self.__UpdateResRect(pos)
        elif self.dnd == 'rect' and self.keydragPosition is None:
            self.__UpdateDragRect(pos)
        elif self.dnd == 'point':
            self.__UpdateDragPoint(pos)
        elif self.dnd == 'line':
            self.__UpdateDragLine(pos)
        # elif self.dnd == 'move':
        #     self.__DrawDragMove(pos)
        # elif self.dnd == 'selection':
        #     self.__DrawDragSel(pos)
        elif self.__NewConnection is not None:
            self.__UpdateNewConnection(pos)
        pass

    def OnMouseDown(self, args):
        """
        Callback for mouse click event.

        @param args: L{DrawingAreaMouseClickEventArgs<lib.Drawing.DrawingAreaMouseClickEventArgs>}
        """
        if args.button == 1 and args.isDoubleClick == True:
            if len(tuple(self.diagram.GetSelection().GetSelected())) == 1:
                for Element in self.diagram.GetSelection().GetSelected():
                    if isinstance(Element, (CElement,CConnection)):
                        self.__OpenSpecification(Element)
                        return True
            elif len(tuple(self.diagram.GetSelection().GetSelected())) == 0:
                self.__OpenSpecification(self.diagram)

        pos = self.GetAbsolutePos(args.position)

        if args.button == 1:
            if self.__toolboxItem != (None, None):
                self.__AddItem(self.__toolboxItem, pos)
                return

            itemSel = self.diagram.GetElementAtPosition(pos)
            if itemSel is not None: #something is hit:
                if itemSel in self.diagram.GetSelection().GetSelected(): # deselecting:
                    if args.IsControlPressed() or args.IsShiftPressed():
                        self.diagram.GetSelection().RemoveFromSelection(itemSel)

                        self.application.GetBus().emit('selected-items', list(self.diagram.GetSelection().GetSelected()))
                    elif isinstance(itemSel, CConnection): #Connection is selected
                         i = itemSel.GetPointAtPosition(pos)
                         if i is not None:
                             itemSel.SelectPoint(i)
                             self.__BeginDragPoint(pos, itemSel, i)
                         else:
                             itemSel.DeselectPoint()
                             i = itemSel.WhatPartOfYouIsAtPosition(pos)
                             self.__BeginDragLine(pos, itemSel, i)
                         self.application.GetBus().emit('selected-items', list(self.diagram.GetSelection().GetSelected()))
                    else: #elements are selected
                        self.__BeginDragRect(pos)
                elif not args.IsControlPressed() and not args.IsShiftPressed():
                    self.diagram.GetSelection().DeselectAll()
                    self.diagram.GetSelection().AddToSelection(itemSel)
                    if isinstance(itemSel, CConnection):
                        i = itemSel.GetPointAtPosition(pos)
                        if i is not None:
                            itemSel.SelectPoint(i)
                            self.__BeginDragPoint(pos, itemSel, i)
                        else:
                            itemSel.DeselectPoint()
                            i = itemSel.WhatPartOfYouIsAtPosition(pos)
                            # self.__BeginDragLine(pos, itemSel, i)
                    else:
                        selElements = list(self.diagram.GetSelection().GetSelectedElements())
                        self.selElem = selElements[0]
                        if len(selElements) == 1:
                            self.selSq = self.diagram.GetSelection().GetSquareAtPosition(pos)
                        self.__BeginDragRect(pos)
            else: # nothing under pointer
                if self.diagram.GetSelection().SelectedCount() > 0:
                    if not args.IsControlPressed():
                        self.diagram.GetSelection().DeselectAll()
                        self.application.GetBus().emit('selected-items', list(self.diagram.GetSelection().GetSelected()))
                # self.__BeginDragSel(pos)

        elif args.button == 2:
            pass
        elif args.button == 3:
            pass

    def OnMouseUp(self, pos):
        pos = self.GetAbsolutePos(pos)

        try:
            if self.dnd == 'resize':
                delta = self.__GetDelta(pos, True)
                self.selElem.Resize(delta, self.selSq)
                self.selElem = None
                self.selSq = None
                self.dnd = None
            elif self.dnd == 'rect':
                delta = self.__GetDelta(pos)
                self.diagram.MoveSelection(delta)
                self.dnd = None
            elif self.dnd == 'point':
                connection, index = self.DragPoint
                self.diagram.MoveConnectionPoint(connection, pos, index)
                self.dnd = None
            elif self.dnd == 'line':
                connection, index = self.DragPoint
                if connection.InsertPoint(pos, index):
                    self.diagram.MoveConnectionPoint(connection, pos, index+1)
                self.dnd = None
            elif self.__NewConnection is not None:
                itemSel = self.diagram.GetElementAtPosition(pos)
                if itemSel is None or isinstance(itemSel, (CConnection, CConLabelInfo)):
                    self.__NewConnection[1].append(pos)
                elif itemSel is not self.__NewConnection[2] or len(self.__NewConnection[1]) > 2:
                    (type, points, source), destination = self.__NewConnection, itemSel
                    obj = CConnectionObject(type, source.GetObject(), destination.GetObject())
                    x = CConnection(self.diagram, obj, source, destination, points[1:])
                    self.application.GetBus().emit('set-selected-toolbox-item', None)
                    self.diagram.GetSelection().AddToSelection(x)
                    self.application.GetBus().emit('selected-items', list(self.diagram.GetSelection().GetSelected()))
                    self.__NewConnection = None
                else:
                    pass

        except ConnectionRestrictionError:
            pass

    def OnToolBoxItemSelected(self, item):
        # set dnd to 'add_obj' ??
        self.__toolboxItem = item
        pass

    def __OpenSpecification(self, obj):
        self.application.GetBus().emit('open-specification', obj)


    def __AddItem(self, toolBtnSel, pos):
        (itemId, itemType) = toolBtnSel

        if itemType == 'Element':
            ElementType = self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(itemId)
            ElementObject = CElementObject(ElementType)
            newElement = CElement(self.diagram, ElementObject)
            newElement.SetPosition(pos)
            self.diagram.MoveElement(newElement, pos)
            # self.AdjustScrollBars()
            self.application.GetBus().emit('set-selected-toolbox-item', None)
            #here, I get prent element of selected elements (if element is on (over) another element)
            minzorder = 9999999
            parentElement = None
            for el in self.diagram.GetSelection().GetSelectedElements(True):
                pos1, pos2 = el.GetSquare()
                zorder = self.diagram.GetElementZOrder(el)
                if newElement.AreYouInRange(pos1, pos2, True):
                    for el2 in self.diagram.GetElementsInRange(pos1, pos2, True):
                        if self.diagram.GetElementZOrder(el2) < minzorder:        #get element with minimal zorder
                            minzorder = self.diagram.GetElementZOrder(el2)
                            parentElement = el2.GetObject()

            self.diagram.GetSelection().DeselectAll()
            self.application.GetBus().emit('add-element', ElementObject, self.diagram, parentElement)
            self.diagram.GetSelection().AddToSelection(newElement)
            self.application.GetBus().emit('selected-items', list(self.diagram.GetSelection().GetSelected()))

        elif itemType == 'Connection':
            itemSel = self.diagram.GetElementAtPosition(pos)

            if itemSel is None:
                if self.__NewConnection is not None:
                    pass
            elif isinstance(itemSel, (CConnection, CConLabelInfo)):
                return
            elif self.__NewConnection is None:
                ConnectionType = self.application.GetProject().GetMetamodel().GetConnectionFactory().GetConnection(itemId)
                center = itemSel.GetCenter()
                self.__NewConnection = (ConnectionType, [center], itemSel)
                self.__UpdateNewConnection(center)
            else:
                pass

    def __GetDelta(self, pos, follow = False):
        if pos == (None, None):
            return 0, 0
        tmpx, tmpy = pos
        dx, dy = tmpx - self.DragStartPos[0], tmpy - self.DragStartPos[1]
        posx, posy = self.DragPoint
        tmpx, tmpy = max(0, posx + dx), max(0, posy + dy)
        return int(tmpx - posx), int(tmpy - posy)

    def __BeginDragRect(self, pos):
        selElements = list(self.diagram.GetSelection().GetSelectedElements())
        self.selElem = selElements[0]
        self.DragStartPos = pos
        if len(selElements) == 1:
            self.selSq = self.diagram.GetSelection().GetSquareAtPosition(self.DragStartPos)
            if(self.setResize == False):
                self.selSq = None
                self.setResize = True
        else:
            self.selSq = None

        self.DragRect = (self.diagram.GetSelectSquare())
        self.DragPoint = list(self.DragRect[0])
        if (self.selSq is None): # Neresizujem
            self.__UpdateDragRect(pos)
            self.dnd = 'rect'
        else:
            self.__UpdateDragRect(pos)
            for i in (0, 1):
                if self.selSq[i] > 0:
                    self.DragPoint[i] += self.DragRect[1][i]
            self.dnd = 'resize'

    def __DrawDragRect(self, canvas):
        if self.selSq is None:
            canvas.DrawRectangle(self.__oldpos, self.DragRect[1], self.dragForegroundColor, None, self.dragLineWidth)

    def __UpdateDragRect(self, pos):
        tmpx, tmpy = self.DragRect[0]
        dx, dy = self.__GetDelta(pos)
        if self.selSq is None:
            x = dx + tmpx
            y = dy + tmpy
            self.__oldpos = x, y


    def __DrawDragSel(self, canvas):
        canvas.DrawRectangle(self.__oldsel[0], self.__oldsel[1], self.dragForegroundColor, None, self.dragLineWidth)

    def __UpdateDragSel(self, pos):
        x1, y1 = self.DragSel
        x2, y2 = self.GetAbsolutePos(pos)
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        tmpx, tmpy = self.GetRelativePos((x1, y1))
        w, h = (x2 - x1), (y2 - y1)
        if self.selSq is None:
            self.__oldsel = tmpx, tmpy, w, h


    def __DrawResRect(self, canvas):
        # seems like x1,x2 should be fixed at starting drag position
        # should be recalculated according to the view port
        canvas.DrawRectangle(self.DragRect[0], self.DragRect[1], self.dragForegroundColor, None, self.dragLineWidth)

    def __UpdateResRect(self, pos):
        delta = self.__GetDelta(pos, True)
        rect = self.selElem.GetResizedRect(delta, self.selSq)
        self.DragRect = rect

    def __UpdateNewConnection(self, (x, y)):
        points = self.__NewConnection[1][:]
        points.append((int(x), int(y)))

        self.__oldNewConnection = points

    def __DrawNewConnection(self, canvas):
        canvas.DrawLines(self.__oldNewConnection, self.dragForegroundColor, line_width=self.dragLineWidth)


    def __BeginDragLine(self, pos, connection, point):
        self.DragStartPos = pos
        self.DragPoint = (connection, point)
        self.__UpdateDragLine(pos)
        self.dnd = 'line'

    def __UpdateDragLine(self, (x, y)):
        if x is None:
            x, y = self.__oldPoints2
        x, y = max(x, 0), max(y, 0)
        connection, index = self.DragPoint
        all = tuple(connection.GetPoints())
        prev, next = all[index], all[index + 1]
        points = [prev, (int(x), int(y)), next]
        self.__oldPoints = points
        self.__oldPoints2 = (x, y)

    def __DrawDragLine(self, canvas):
        canvas.DrawLines(self.__oldPoints, self.dragForegroundColor, line_width=self.dragLineWidth)

    def __BeginDragPoint(self, pos, connection, point):
        self.DragStartPos = pos
        self.DragPoint = (connection, point)
        self.__UpdateDragPoint(pos)
        self.dnd = 'point'

    def __UpdateDragPoint(self, (x, y)):
        if x is None:
            x, y = self.__oldPoints2
        connection, index = self.DragPoint
        prev, next = connection.GetNeighbours(index)
        x, y = max(x, 0), max(y, 0)
        points = [prev, (int(x), int(y)), next]
        self.__oldPoints = points
        self.__oldPoints2 = (x, y)

    def __DrawDragPoint(self, canvas):
        canvas.DrawLines(self.__oldPoints, self.dragForegroundColor, line_width=self.dragLineWidth)