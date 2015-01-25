from lib.Base import CBaseObject
from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand
from lib.Drawing.DrawingAreaKeyPressEventArgs import KEY_A, KEY_DELETE, KEY_ESCAPE, KEY_SPACE, KEY_RIGHT, KEY_LEFT, \
    KEY_UP, KEY_DOWN

from lib.Elements import CElementObject
from lib.Connections import CConnectionObject
from lib.Drawing import CDiagram, CConnection, CElement, CConLabelInfo
from lib.Drawing.DiagramExporter import CDiagramExporter
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
        self.physicalViewPort = ((0, 0), (0, 0))
        self.virtualAreaBounds = ((0, 0), BUFFER_SIZE)
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

    def GetDiagram(self):
        """
        Returns associated diagram.

        @return: Associated diagram
        @rtype:  L{Diagram<Diagram>}
        """
        return self.diagram

    def GetDiagramPhysicalSize(self):
        tmp = [int(max(i)) for i in zip(self.TupleToPhysical(self.diagram.GetSize()), self.GetPhysicalViewPortSize())]
        return tuple(tmp)

    def GetVirtualAreaBounds(self):
        """
        Returns bounds of virtual drawing area.

        @return: Rectangle representing bounds of virtual drawing area. Two tuples (x, y), (width, height).
        @rtype : tuple
        """
        return self.virtualAreaBounds

    def GetLogicalViewPort(self):
        """
        Returns current logical view port.

        Converts physical view port to logical units.

        @return: Rectangle representing current logical view port. Two tuples (x, y), (width, height).
        @rtype: tuple
        """

        pos, size = self.GetPhysicalViewPort()

        pos = self.TupleToLogical(pos)
        size = self.TupleToLogical(size)
        return (pos, size)

    def SetLogicalViewPort(self, viewPort):
        """
        Changes current view port.

        @param viewPort: Rectangle representing new view port. Two tuples (x, y), (width, height).
        @type viewPort: tuple

        @rtype: bool
        @return: True, if drawing area needs to be resized, False if not.
        """
        (pos, size) = viewPort
        pos = self.TupleToPhysical(pos)
        size = self.TupleToPhysical(size)

        return self.SetPhysicalViewPort((pos, size))

    def GetPhysicalViewPort(self):
        """
        Returns current physical view port.

        @return: Rectangle representing current physical view port. Two tuples (x, y), (width, height).
        @rtype: tuple
        """
        return self.physicalViewPort

    def SetPhysicalViewPort(self, viewPort):
        """
        Changes current physical view port. Value is converted to logical units.

        @param viewPort: Rectangle representing new physical view port. Two tuples (x, y), (width, height).
        @type viewPort: tuple

        @rtype: bool
        @return: True, if drawing area needs to be resized, False if not.
        """

        (x, y), (w, h) = viewPort

        (dw, dh) = self.GetDiagramPhysicalSize()

        # don't allow scrolling outside of view port or diagram size
        (x, y) = min(dw - w, x), min(dh - h, y)

        # don't allow scrolling  beyond 0, 0 position
        (x, y) = max(0, x), max(0, y)

        self.physicalViewPort = ((x, y), (w, h))
        return self.__UpdateDrawingBuffer(self.physicalViewPort)

    def GetLogicalViewPortPos(self):
        """
        Returns logical view port position.

        @return: Position of the view port.
        @rtype : tuple
        """
        pos = self.GetPhysicalViewPortPos()
        return self.TupleToLogical(pos)

    def SetLogicalViewPortPos(self, pos):
        """
        Changes logical view port position.

        Coordinates are converted to physical units.

        @param pos: New logical view port position
        @type pos: tuple
        """
        size = self.GetLogicalViewPortSize()
        self.SetLogicalViewPort((pos, size))

    def GetPhysicalViewPortPos(self):
        """
        Returns physical view port position.

        @return: Position of the physical view port.
        @rtype : tuple
        """
        return self.physicalViewPort[0]

    def SetPhysicalViewPortPos(self, pos):
        """
        Changes physical view port position.

        Coordinates are converted to logical units.

        @param pos: New physical view port position
        @type pos: tuple
        """
        size = self.GetPhysicalViewPortSize()
        self.SetPhysicalViewPort((pos, size))

    def GetLogicalViewPortSize(self):
        """
        Returns logical view port size.

        @return: Size of the logical view port
        @rtype : tuple
        """
        size = self.GetPhysicalViewPortSize()
        return self.TupleToLogical(size)

    def SetLogicalViewPortSize(self, size):
        """
        Changes logical view port size.

        Size is converted to physical units.

        @param size: New logical size of the view port
        @type size: tuple
        """
        pos = self.GetLogicalViewPortPos()
        self.SetLogicalViewPort((pos, size))

    def GetPhysicalViewPortSize(self):
        """
        Returns physical view port size.

        @return: Size of the physical view port
        @rtype : tuple
        """
        return self.physicalViewPort[1]

    def SetPhysicalViewPortSize(self, size):
        """
        Changes physical view port size.

        @param size: New physical size of the view port
        @type size: tuple
        """
        pos = self.GetPhysicalViewPortPos()
        self.SetPhysicalViewPort((pos, size))

    def TupleToPhysical(self, pos):
        """
        Converts logical coordinates to physical.

        @param pos: Coordinates to convert.
        @type pos: tuple

        @return: Coordinates in physical units.
        @rtype : tuple
        """
        return PositionToPhysical(pos, self.scale)

    def TupleToLogical(self, pos):
        """
        Converts physical coordinates to logical.

        @param pos: Coordinates to convert.
        @type pos: tuple

        @return: Coordinates in logical units.
        @rtype : tuple
        """
        return PositionToLogical(pos, self.scale)

    def OffsetOnVirtualArea(self, pos):
        """
        Offsets specified position inside virtual drawing area.

        @param pos: Position to offset
        @type pos : tuple

        @rtype : tuple
        @return: Position offset on virtual drawing area.
        """
        virtualAreaPos = self.virtualAreaBounds[0]
        return pos[0] - virtualAreaPos[0], pos[1] - virtualAreaPos[1]

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
        (x, y) = self.TupleToLogical((posx, posy))
        (dx, dy) = self.GetLogicalViewPortPos()
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
        (x, y) = self.TupleToPhysical((posx, posy))
        (dx, dy) = self.GetPhysicalViewPortPos()
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

    def BestFitScale(self):
        viewPortSizeX, viewPortSizeY = self.GetLogicalViewPortSize()
        (diaSizeMinX, diaSizeMinY), (diaSizeMaxX, diaSizeMaxY) = self.diagram.GetSizeSquare()
        scaleX = float(viewPortSizeX) / float(diaSizeMaxX-diaSizeMinX)
        scaleY = float(viewPortSizeY) / float(diaSizeMaxY-diaSizeMinY)
        if scaleX > scaleY:
            scale = scaleY
        else:
            scale = scaleX

        if scale < SCALE_MIN:
            scale = SCALE_MIN
        elif scale > SCALE_MAX:
            scale = SCALE_MAX

        self.SetScale(scale)
        viewPortPos = (diaSizeMinX, diaSizeMinY)
        self.SetLogicalViewPortPos(viewPortPos)

    def Paint(self, canvas, changed = True):
        """
        Paints diagram at canvas

        @param canvas: Canvas on which its being drawn
        @type  canvas: L{CCairoCanvas<lib.Drawing.Canvas.CairoCanvas.CCairoCanvas>}
        """

        canvas.SetScale(self.scale)

        if changed:

            # When drawing area is zoomed in, the virtual area is shrank (and vice versa)
            # the reason is that the canvas has always the same size.

            # We need to calculate logical bounds of the virtual area.

            virtual_area_offset = self.TupleToLogical(self.virtualAreaBounds[0])
            virtual_area_size = self.TupleToLogical(self.virtualAreaBounds[1])

            logical_virtual_area_bounds = (virtual_area_offset, virtual_area_size)

            self.diagram.Paint(canvas, logical_virtual_area_bounds)

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
                    self.diagram.GetSelection().DeselectAll()
                    return
        for sel in self.diagram.GetSelection().GetSelected():
            self.diagram.DeleteItem(sel)
        self.diagram.GetSelection().DeselectAll()
        self.__OnSelectionUpdated()

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
        for sel in self.diagram.GetSelection().GetSelected():
            if isinstance(sel, CElement):
                self.emit('delete-element-from-all',sel.GetObject())
            elif isinstance(sel, CConLabelInfo):
                self.diagram.ShiftDeleteConLabel(sel)
            else:
                self.diagram.ShiftDeleteConnection(sel)

    def ChangeConnectionSourceTarget(self):
        """
        Switches source and target of selected connections (L{CConnectionObject<lib.Connections.CConnectionObject>}).
        This also switches L{CConnection<lib.Drawing.CConnection> in all diagrams, that contain given connection.
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

    def Export(self, filename, export_type, zoom, padding, background=None):
        exporter = CDiagramExporter(self.application.GetProject().GetMetamodel().GetStorage(), export_type)
        exporter.SetZoom(zoom)
        exporter.SetPadding(padding)
        exporter.SetBackground(background)
        exporter.ExportDiagram(self.diagram, filename)

    def __UpdateDrawingBuffer(self, viewport):
        posx, posy = viewport[0]
        sizx, sizy = viewport[1]

        ((bposx, bposy), (bsizx, bsizy)) = self.virtualAreaBounds

        bufferResized = False

        # resize buffer rectangle, if we get out of its bounds
        if posx < bposx or bposx + bsizx < posx + sizx or \
           posy < bposy or bposy + bsizy < posy + sizy:

            bposx = posx + (sizx - bsizx)//2
            bposy = posy + (sizy - bsizy)//2

            bposx = max(bposx, 0)
            bposy = max(bposy, 0)

            self.virtualAreaBounds = ((bposx, bposy), (bsizx, bsizy))

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
        posx, posy = self.GetLogicalViewPortPos()
        x1, y1 = pos
        x2, y2 = self.DragStartPos
        self.SetLogicalViewPortPos((posx - x1 + x2, posy - y1 + y2))

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
            self.__DrawRectangle(canvas, (self.__oldpos, self.DragRect[1]), self.dragForegroundColor, None, self.dragLineWidth)


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
        self.__DrawRectangle(canvas, (pos, size), self.dragForegroundColor, None, self.dragLineWidth)


    def __DrawResRect(self, canvas):
        # seems like x1,x2 should be fixed at starting drag position
        # should be recalculated according to the view port
        rectangle = (self.DragRect[0], self.DragRect[1])
        self.__DrawRectangle(canvas, rectangle, self.dragForegroundColor, None, self.dragLineWidth)

    def __UpdateResRect(self, pos):
        delta = self.__GetDelta(pos, True)
        rect = self.selElem.GetResizedRect(delta, self.selSq)
        self.DragRect = rect

    def __UpdateNewConnection(self, (x, y)):
        points = self.__NewConnection[1][:]
        points.append((int(x), int(y)))

        self.__oldNewConnection = points

    def __DrawNewConnection(self, canvas):
        self.__DrawLines(canvas, self.__oldNewConnection, self.dragForegroundColor, self.dragLineWidth)


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
        self.__DrawLines(canvas, self.__oldPoints, self.dragForegroundColor, self.dragLineWidth)

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
        self.__DrawLines(canvas, self.__oldPoints, self.dragForegroundColor, self.dragLineWidth)

    def __DrawRectangle(self, canvas, (pos, size), foregroundColor, backgroundColor, lineWidth):
        offsetPos = self.__OffsetLogicalPointOnVirtualArea(pos)
        canvas.DrawRectangle(offsetPos, size, foregroundColor, backgroundColor, lineWidth)

    def __DrawLines(self, canvas, points, foregroundColor, line_width):
        offsetPoints = (self.__OffsetLogicalPointOnVirtualArea(p) for p in points)
        canvas.DrawLines(offsetPoints, foregroundColor, line_width)

    def __OffsetLogicalPointOnVirtualArea(self, (x, y)):
        (bX, bY) = self.TupleToLogical(self.virtualAreaBounds[0])
        return (x - bX, y - bY)

    def __ResetAction(self):
        self.dnd = None
        if self.__NewConnection is not None:
            self.__NewConnection = None

    def __OnSelectionUpdated(self):
        self.application.GetBus().emit('selected-items', list(self.diagram.GetSelection().GetSelected()))

    def __CenterZoom(self, scale):
        positionH = 0.0
        positionW = 0.0
        shift = 0
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

            x, y = self.GetLogicalViewPortPos()
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

            self.SetLogicalViewPortPos((int(x), int(y)))

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
        posx, posy = self.GetLogicalViewPortPos()
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
        self.SetLogicalViewPortPos((posx, posy))
        self.setResize = False
        self.__viewPortPlusMove = 0