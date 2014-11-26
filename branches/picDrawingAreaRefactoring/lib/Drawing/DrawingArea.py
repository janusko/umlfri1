from lib.Base import CBaseObject
from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand

from lib.Drawing import CDiagram, CConnection, CElement, CConLabelInfo
from lib.Drawing.DrawingHelper import PositionToPhysical, PositionToLogical

from lib.Gui.common import CGuiObject

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

        self.dragForegroundColor = config['/Styles/Drag/RectangleColor'].Invert()
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

        # if self.dnd == 'resize':
        #     self.__DrawResRect(None, True, True)
        # elif self.dnd == 'rect' and self.keydragPosition is None:
        #     self.__DrawDragRect(pos)
        # elif self.dnd == 'point':
        #     self.__DrawDragPoint(pos)
        # elif self.dnd == 'line':
        #     self.__DrawDragLine(pos)
        # elif self.dnd == 'move':
        #     self.__DrawDragMove(pos)
        # elif self.dnd == 'selection':
        #     self.__DrawDragSel(pos)
        # elif self.__NewConnection is not None:
        #     self.__DrawNewConnection(pos)

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
        # if self.dnd == 'resize':
        #     self.__DrawResRect(pos, True, True)
        # elif self.dnd == 'rect' and self.keydragPosition is None:
        #     self.__DrawDragRect(pos)
        # elif self.dnd == 'point':
        #     self.__DrawDragPoint(pos)
        # elif self.dnd == 'line':
        #     self.__DrawDragLine(pos)
        # elif self.dnd == 'move':
        #     self.__DrawDragMove(pos)
        # elif self.dnd == 'selection':
        #     self.__DrawDragSel(pos)
        # elif self.__NewConnection is not None:
        #     self.__DrawNewConnection(pos)
        pass

    def OnMouseClick(self, args):
        """
        Callback for mouse click event.

        @param args: L{DrawingAreaMouseClickEventArgs<lib.Drawing.DrawingAreaMouseClickEventArgs>}
        """
        if args.button == 1 and args.isDoubleClick == True:
            if len(tuple(self.diagram.GetSelection().GetSelected())) == 1:
                for Element in self.diagram.GetSelected():
                    if isinstance(Element, (CElement,CConnection)):
                        self.__OpenSpecification(Element)
                        return True
            elif len(tuple(self.diagram.GetSelection().GetSelected())) == 0:
                self.__OpenSpecification(self.diagram)

    def OnToolBoxItemSelected(self, item):
        # set dnd to 'add_obj' ??
        pass

    def __OpenSpecification(self, obj):
        self.application.GetBus().emit('open-specification', obj)

    def __GetDelta(self, pos, follow = False):
        if pos == (None, None):
            return 0, 0
        tmpx, tmpy = self.GetAbsolutePos(pos)
        dx, dy = tmpx - self.DragStartPos[0], tmpy - self.DragStartPos[1]
        posx, posy = self.DragPoint
        tmpx, tmpy = max(0, posx + dx), max(0, posy + dy)
        return int(tmpx - posx), int(tmpy - posy)

    def __DrawNewConnection(self, canvas):
        pass

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

    def __DrawDragSel(self, canvas):
        canvas.DrawRectangle(self.__oldsel[0], self.__oldsel[1], self.dragForegroundColor, None, self.dragLineWidth)
