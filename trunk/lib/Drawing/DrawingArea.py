from lib.Base import CBaseObject
from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand

from lib.Drawing import CDiagram, CConnection, CElement, CConLabelInfo
from lib.Drawing.DrawingHelper import PositionToPhysical, PositionToLogical

from lib.Gui.common import CGuiObject
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
        self.paintlock = thread.allocate()
        self.toBePainted = False
        self.paintChanged = False

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
            self.canvas.SetScale(self.scale)
            # self.AdjustScrollBars()
            self.disablePaint = False
            self.Paint()

    def ToPaint(self, changed = True):
        try:
            self.paintlock.acquire()
            self.paintChanged = self.paintChanged or changed
            if not self.toBePainted:
                self.toBePainted = True
                gobject.timeout_add(15, self.Paint)
        finally:
            self.paintlock.release()

    def Paint(self, canvas, changed = True):
        """
        Paints diagram at canvas

        @param canvas: Canvas on which its being drawn
        @type  canvas: L{CCairoCanvas<lib.Drawing.Canvas.CairoCanvas.CCairoCanvas>}
        """

        if self.disablePaint:
            return
        try:
            self.paintlock.acquire()
            self.toBePainted = False
            changed = changed or self.paintChanged
            self.paintChanged = False
        finally:
            self.paintlock.release()

        if changed:
            self.canvas.SetScale(self.scale)

            self.diagram.Paint(self.canvas)

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

        bufferResized = False

        # resize buffer rectangle, if we get out of its bounds
        if posx < bposx or bposx + bsizx < posx + sizx or \
           posy < bposy or bposy + bsizy < posy + sizy:

            bposx = posx + (sizx - bsizx)//2
            bposy = posy + (sizy - bsizy)//2

            self.buffer_size = ((bposx, bposy), (bsizx, bsizy))

            bufferResized = True

        return bufferResized