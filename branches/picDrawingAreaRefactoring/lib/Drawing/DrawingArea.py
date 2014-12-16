from lib.Base import CBaseObject
from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand
from lib.Drawing.DrawingAreaKeyPressEventArgs import KEY_A, KEY_DELETE, KEY_ESCAPE, KEY_SPACE, KEY_RIGHT, KEY_LEFT, \
    KEY_UP, KEY_DOWN

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

        self.__viewPortShiftDirection = ""
        self.__viewPortPlusMove = 0

        self.__NewConnection = None

        self.__oldsel = None

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

    def SetViewPortPos(self, (x, y) = (0, 0)):
        """
        Changes view port position.

        @param pos: New view port position
        @type pos: tuple
        """
        size = (w, h) = self.GetViewPortSize()
        (dw, dh) = self.GetDiagramSize()

        # don't allow scrolling outside of view port or diagram size
        (x, y) = min(dw - w, x), min(dh - h, y)

        # don't allow scrolling  beyond 0, 0 position
        pos = max(0, x), max(0, y)
        self.viewPort = pos, size

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

    def GetDiagramSize(self):
        tmp = [int(max(i)) for i in zip(self.diagram.GetSize(), self.GetViewPortSize())]
        return tuple(tmp)

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
        (x, y) = PositionToLogical((posx, posy), self.scale)
        (dx, dy) = PositionToLogical(self.GetViewPortPos(), self.scale)
        return (x + dx, y + dy)

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
        (x, y) = PositionToPhysical((posx, posy), self.scale)
        (dx, dy) = PositionToPhysical(self.GetViewPortPos(), self.scale)
        return (x - dx, y - dy)

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

    def IncScale(self, scale):
        """
        Increases or decreases scale (zoom) based on @scale.

        @param scale: Specifies, whether the scale is increased or decreased.
        @type scale: float
        """
        tmp_scale = (SCALE_INCREASE*((self.scale+0.00001)//SCALE_INCREASE))+scale
        if (tmp_scale+0.00001 >= SCALE_MIN) and (tmp_scale-0.00001 <= SCALE_MAX):
            self.scale = tmp_scale
            self.__CenterZoom(scale)

    def Paint(self, canvas, changed = True):
        """
        Paints diagram at canvas

        @param canvas: Canvas on which its being drawn
        @type  canvas: L{CCairoCanvas<lib.Drawing.Canvas.CairoCanvas.CCairoCanvas>}
        """

        canvas.SetScale(self.scale)

        if changed:
            self.diagram.Paint(canvas, self.buffer_size)

        if self.__viewPortShiftDirection != "":
            self.__ShiftViewPort(self.__viewPortShiftDirection)
            self.__viewPortShiftDirection = ""

        if self.dnd == 'resize':
            self.__DrawResRect(canvas)
        if self.dnd == 'rect':
            self.__DrawDragRect(canvas)
        elif self.dnd == 'point':
            self.__DrawDragPoint(canvas)
        elif self.dnd == 'line':
            self.__DrawDragLine(canvas)
        elif self.dnd == 'selection':
            self.__DrawDragSel(canvas)
        elif self.__NewConnection is not None:
            self.__DrawNewConnection(canvas)

    def SelectAll(self):
        """
        Selects all elements and connections in the diagram.

        """
        self.diagram.GetSelection().SelectAll(self.diagram.GetElements(), self.diagram.GetConnections())

    def DeleteSelectedObjects(self):
        """
        Deletes all currently selected objects.
        """
        for sel in self.diagram.GetSelection().GetSelected():
            if isinstance(sel, CConnection):
                index = sel.GetSelectedPoint()
                if index is not None and (sel.GetSource() != sel.GetDestination() or len(tuple(sel.GetMiddlePoints())) > 2):
                    sel.RemovePoint(index)
                    self.diagram.DeselectAll()
                    self.Paint()
                    return
        for sel in self.diagram.GetSelection().GetSelected():
            self.diagram.DeleteItem(sel)
        self.diagram.DeselectAll()
        self.emit('selected-item', list(self.diagram.GetSelection().GetSelected()),False)
        self.Paint()

    def ShiftElements(self, actionName):
        """
        Shifts selected elements' z-order based on argument.

        @param actionName: target position, where the element should be shifted.
        @type actionName: str
        """
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
        """
        Copies selected objects to clipboard.
        """
        self.diagram.CopySelection(self.application.GetClipboard())

    def CutSelectedObjects(self):
        """
        Cuts selected objects from diagram into clipboard.
        """
        self.diagram.CutSelection(self.application.GetClipboard())
        self.__OnSelectionUpdated()

    def PasteObjects(self):
        """
        Pastes objects from clipboard into diagram.
        """
        self.diagram.PasteSelection(self.application.GetClipboard())
        self.__OnSelectionUpdated()

    def DuplicateSelectedObjects(self):
        """
        Duplicates selected objects.
        """
        cmd  = CDuplicateElementsCommand(tuple(self.diagram.GetSelection().GetSelectedElements()), self.diagram)
        self.application.GetCommands().Execute(cmd)

    def ShiftDeleteSelectedObjects(self):
        """
        "Shift" deletes selected objects, i.e. removes them from project, not just from current diagram.
        """
        for sel in self.diagram.GetSelected():
            if isinstance(sel, CElement):
                self.emit('delete-element-from-all',sel.GetObject())
            elif isinstance(sel, CConLabelInfo):
                self.diagram.ShiftDeleteConLabel(sel)
            else:
                self.diagram.ShiftDeleteConnection(sel)

    def ChangeConnectionSourceTarget(self):
        """
        Switches source and target of selected connections (L{CConectionObject<lib.Connections.CConectionObject>}).
        This also switches L{CConection<lib.Drawing.CConnection> in all diagrams, that contain given connection.
        """
        for sel in self.diagram.GetSelection().GetSelected():
            if isinstance(sel, CConnection):
                sel.GetObject().ChangeConnection()
            project = self.application.GetProject()
            diagrams = project.GetDiagrams()
            for d in diagrams:
                for c in d.GetConnections():
                    if c.GetObject() == sel.GetObject():
                        c.ChangeConnection()

    def Align(self, isHorizontal, isLowerBoundary, alignToSelectedElement=True):
        """
        Aligns selected elements along specified axis and position.
        If position isn't set, elements will be aligned to their average
        position.

        @param isHorizontal: align horizontally or vertically
        @type isHorizontal: bool
        @param isLowerBoundary: align to lower or higher boundary
        @type isLowerBoundary: bool
        @param alignToSelectedElement: If True, aligning is done to selected element, False otherwise.
        @type alignToSelectedElement: bool
        """
        self.diagram.AlignElementsXY(isHorizontal, alignToSelectedElement, self.itemSel if alignToSelectedElement else None)

    def AlignCenter(self, isHorizontal, alignToSelectedElement = True):
        """
        Aligns centers of selected elements to defaultElements center
        along x or y axis.
        If defaultElement it's set, elements will be aligned to their average
        center position.

        @param isHorizontal: align horizontally or vertically
        @type isHorizontal: bool
        @param alignToSelectedElement: If True, aligning is done to selected element, False otherwise.
        @type alignToSelectedElement: bool
        """
        self.diagram.AlignElementCentersXY(isHorizontal, self.itemSel if alignToSelectedElement else None)

    def ResizeHeight(self):
        """
        Resize selected elements evenly to minimal or maximal height of selected
        elements or requested height.
        """
        self.diagram.ResizeElementsEvenly(False, self.itemSel)

    def ResizeWidth(self):
        """
        Resize selected elements evenly to minimal or maximal width of selected
        elements or requested width.
        """
        self.diagram.ResizeElementsEvenly(True, self.itemSel)

    def ResizeWidthAndHeight(self):
        """
        Resize selected elements evenly to minimal or maximal size of selected
        elements or requested size.
        """
        self.diagram.ResizeElementsEvenly(True, self.itemSel)
        self.diagram.ResizeElementsEvenly(False, self.itemSel)

    def ResizeByMaximalElement(self):
        """
        Resize all elements based on the size of the maximal element
        """
        self.diagram.ResizeByMaximalElement()

    def ResizeByMinimalElement(self):
        """
        Resize all elements based on the size of the minimal element
        """
        self.diagram.ResizeByMinimalElement()

    def SnapSelected(self):
        self.diagram.SnapElementsOnGrid()

    def MakeSpacing(self, isHorizontal):
        self.diagram.SpaceElementsEvenlyXY(isHorizontal)

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
        elif self.dnd == 'move':
            self.__UpdateDragMove(pos)
        elif self.dnd == 'selection':
            self.__UpdateDragSel(pos)
        elif self.__NewConnection is not None:
            self.__UpdateNewConnection(pos)
        pass

    def OnMouseDown(self, args):
        """
        Callback for mouse click event.

        @param args: L{DrawingAreaMouseDownEventArgs<lib.Drawing.DrawingAreaMouseDownEventArgs>}
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
            if args.wasSpacePressed:
                self.__BeginDragMove(pos)
                return True

            if self.__toolboxItem != (None, None):
                self.__AddItem(self.__toolboxItem, pos)
                return

            itemSel = self.diagram.GetElementAtPosition(pos)
            if itemSel is not None: #something is hit:
                if itemSel in self.diagram.GetSelection().GetSelected(): # deselecting:
                    if args.IsControlPressed() or args.IsShiftPressed():
                        self.diagram.GetSelection().RemoveFromSelection(itemSel)

                        self.__OnSelectionUpdated()
                    elif isinstance(itemSel, CConnection): #Connection is selected
                         i = itemSel.GetPointAtPosition(pos)
                         if i is not None:
                             itemSel.SelectPoint(i)
                             self.__BeginDragPoint(pos, itemSel, i)
                         else:
                             itemSel.DeselectPoint()
                             i = itemSel.WhatPartOfYouIsAtPosition(pos)
                             self.__BeginDragLine(pos, itemSel, i)
                         self.__OnSelectionUpdated()
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
                            self.__BeginDragLine(pos, itemSel, i)
                    else:
                        selElements = list(self.diagram.GetSelection().GetSelectedElements())
                        self.selElem = selElements[0]
                        if len(selElements) == 1:
                            self.selSq = self.diagram.GetSelection().GetSquareAtPosition(pos)
                        self.__BeginDragRect(pos)
                    self.__OnSelectionUpdated()
                else:
                    self.diagram.GetSelection().AddToSelection(itemSel)
                    self.__OnSelectionUpdated()
            else: # nothing under pointer
                if self.diagram.GetSelection().SelectedCount() > 0:
                    if not args.IsControlPressed():
                        self.diagram.GetSelection().DeselectAll()
                        self.__OnSelectionUpdated()
                self.__BeginDragSel(pos)

        elif args.button == 2:
            self.__BeginDragMove(pos)

        elif args.button == 3:
            itemSel = self.diagram.GetElementAtPosition(pos)
            if itemSel not in frozenset(self.diagram.GetSelection().GetSelected()):
                self.diagram.GetSelection().DeselectAll()
            if itemSel is not None:
                self.diagram.GetSelection().AddToSelection(itemSel)
            self.__OnSelectionUpdated()
            self.itemSel = itemSel

    def OnMouseUp(self, args):
        """
        Callback for mouse release event.

        @param args: L{DrawingAreaMouseUpEventArgs<lib.Drawing.DrawingAreaMouseUpEventArgs>}
        """
        pos = args.position

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
            elif self.dnd == 'move':
                if args.wasSpacePressed:
                    self.cursor = 'grab'
                else:
                    self.cursor = None
                self.dnd = None
            elif self.dnd == 'selection':
                x1, y1 = self.DragSel
                x2, y2 = pos
                if x2 < x1:
                    x2, x1 = x1, x2
                if y2 < y1:
                    y2, y1 = y1, y2
                self.diagram.AddRangeToSelection((x1, y1), (x2, y2))
                self.dnd = None
                self.__OnSelectionUpdated()
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
                    self.__OnSelectionUpdated()
                    self.__NewConnection = None
                else:
                    pass

        except ConnectionRestrictionError:
            self.__ResetAction()
            self.__ClearSelectedToolBoxItem()
            self.application.GetBus().emit('run-dialog', 'warning', _('Invalid connection'))

    def OnKeyPress(self, args):
        """
        Callback for key press event.

        @param args: L{DrawingAreaKeyPressEventArgs<lib.Drawing.DrawingAreaKeyPressEventArgs>}
        """
        if args.IsControlPressed() and args.IsKeyPressed(KEY_A):
            self.SelectAll()
            self.__OnSelectionUpdated()
        elif args.IsKeyPressed(KEY_DELETE):
            if self.dnd is not None:
                return
            if args.IsShiftPressed():
                for sel in self.diagram.GetSelection().GetSelected():
                    if isinstance(sel, CElement):
                        self.application.GetBus().emit('delete-element-from-all', sel.GetObject())
                    else:
                        self.diagram.ShiftDeleteConnection(sel)
            else:
                for sel in self.diagram.GetSelection().GetSelected():
                    self.diagram.DeleteItem(sel)

                self.__OnSelectionUpdated()
        elif args.IsKeyPressed(KEY_ESCAPE):
            self.__ResetAction()
            self.__ClearSelectedToolBoxItem()
        elif args.IsKeyPressed(KEY_SPACE):
            self.cursor = 'grab'
        elif args.IsArrowKeyPressed():
            selected = list(self.diagram.GetSelection().GetSelectedElements())
            if selected:
                if self.dnd is None:
                    self.keydragPosition = list(selected[0].GetCenter())

                    self.__BeginDragRect(self.keydragPosition[:])
                if self.dnd == 'rect':
                    if self.keydragPosition is None:
                        self.keydragPosition = list(selected[0].GetCenter())
                    if args.IsKeyPressed(KEY_RIGHT):
                        diff = 10 + self.__GetPlusMove("hor")
                        self.keydragPosition[0] += diff
                        self.__SetDelayedViewPortShift("right")
                        self.__SetViewPortPlusMove(diff)
                    if args.IsKeyPressed(KEY_LEFT):
                        diff = 10 + self.__GetPlusMove("hor")
                        self.keydragPosition[0] -= diff
                        self.__SetDelayedViewPortShift("left")
                        self.__SetViewPortPlusMove(diff)
                    if args.IsKeyPressed(KEY_UP):
                        diff = 10 + self.__GetPlusMove("ver")
                        self.keydragPosition[1] -= diff
                        self.__SetDelayedViewPortShift("up")
                        self.__SetViewPortPlusMove(diff)
                    if args.IsKeyPressed(KEY_DOWN):
                        diff = 10 + self.__GetPlusMove("ver")
                        self.keydragPosition[1] += diff
                        self.__SetDelayedViewPortShift("down")
                        self.__SetViewPortPlusMove(diff)
                    self.__UpdateDragRect(self.keydragPosition)

    def OnKeyUp(self, args):
        """
        Callback for key release event.

        @param args: L{CDrawingAreaKeyUpEventArgs<lib.Drawing.CDrawingAreaKeyUpEventArgs>}
        """
        if args.IsKeyPressed(KEY_SPACE) == False:
            if self.dnd != 'move':
                self.cursor = None

        if args.WasArrowKeyPressed() and self.dnd == 'rect':
            delta = self.__GetDelta(self.keydragPosition)
            self.keydragPosition = None
            self.diagram.MoveSelection(delta)
            self.dnd = None

    def OnToolBoxItemSelected(self, item):
        """
        Callback for selected-toolbox-item-changed event (i.e. when item is selected in toolbox on the left).
        """
        # set dnd to 'add_obj' ??
        self.__toolboxItem = item
        pass

    def OnLostFocus(self):
        """
        Callback for focus out event.
        """
        self.__ClearSelectedToolBoxItem()
        self.__ResetAction()

    def __ClearSelectedToolBoxItem(self):
        self.application.GetBus().emit('set-selected-toolbox-item', None)

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
            self.__OnSelectionUpdated()

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

    def __BeginDragMove(self, pos):
        self.cursor = 'grabbing'
        self.DragStartPos = pos
        self.dnd = 'move'

    def __UpdateDragMove(self, pos):
        posx, posy = self.GetViewPortPos()
        x1, y1 = pos
        x2, y2 = self.DragStartPos
        self.SetViewPortPos((posx - x1 + x2, posy - y1 + y2))

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

    def __UpdateDragRect(self, pos):
        tmpx, tmpy = self.DragRect[0]
        dx, dy = self.__GetDelta(pos)
        if self.selSq is None:
            x = dx + tmpx
            y = dy + tmpy
            self.__oldpos = x, y

    def __DrawDragRect(self, canvas):
        if self.selSq is None:
            canvas.DrawRectangle(self.__oldpos, self.DragRect[1], self.dragForegroundColor, None, self.dragLineWidth)


    def __BeginDragSel(self, pos):
        self.DragSel = pos
        self.__UpdateDragSel(pos)
        self.dnd = 'selection'

    def __UpdateDragSel(self, pos):
        x1, y1 = self.DragSel
        x2, y2 = pos
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        w, h = (x2 - x1), (y2 - y1)
        if self.selSq is None:
            self.__oldsel = (x1, y1), (w, h)

    def __DrawDragSel(self, canvas):
        pos, size = self.__oldsel
        canvas.DrawRectangle(pos, size, self.dragForegroundColor, None, self.dragLineWidth)


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

    def __ResetAction(self):
        self.dnd = None
        if self.__NewConnection is not None:
            self.__NewConnection = None

    def __OnSelectionUpdated(self):
        self.application.GetBus().emit('selected-items', list(self.diagram.GetSelection().GetSelected()))

    def __CenterZoom(self, scale):
        positionH = 0.0
        positionW = 0.0
        shift = 180
        elements = tuple(self.diagram.GetSelection().GetSelectedElements())
        if (len(elements)>0):
            avgH = 0
            avgW = 0
            for e in elements:
                avgW += e.GetCenter()[0]
                avgH += e.GetCenter()[1]
            avgH = avgH/len(elements)
            avgW = avgW/len(elements)
            positionH = avgH/5.0
            positionW = avgW/5.0

            x, y = self.GetViewPortPos()
            if(scale > 0): #INZOOM
                if(avgH>shift):
                    y += positionH
                else:
                    y = 0
                if(avgW>shift):
                    x += positionW
                else:
                    x = 0
            else: #OUTZOOM
                if(avgH>shift):
                    y -= positionH
                else:
                    y = 0
                if(avgW>shift):
                    x -= positionW
                else:
                    x = 0

            self.SetViewPortPos((x, y))

    def __GetPlusMove(self, horVer):
        active = config['/Grid/Active']
        hor_spacing = config['/Grid/HorSpacing']
        ver_spacing = config['/Grid/VerSpacing']

        plusmove = 0
        if(active == "true"):
            if((horVer == "hor") & (hor_spacing >= 10)):
                plusmove = (hor_spacing - 10)
            if((horVer == "ver") & (ver_spacing >= 10)):
                plusmove = (ver_spacing - 10)
        return plusmove

    def __SetViewPortPlusMove(self, plusMove):
        self.__viewPortPlusMove = plusMove

    def __SetDelayedViewPortShift(self, direction):
        self.__viewPortShiftDirection = direction

    def __ShiftViewPort(self, direction):
        posx, posy = self.GetViewPortPos()
        if(self.__viewPortPlusMove > 0):
            move = int(self.__viewPortPlusMove / 2)
        else:
            move = 5
        if(direction == "right"):
            posx += move
        if(direction == "left"):
            posx -= move
        if(direction == "up"):
            posy -= move
        if(direction == "down"):
            posy += move
        self.SetViewPortPos((posx, posy))
        self.setResize = False
        self.__viewPortPlusMove = 0