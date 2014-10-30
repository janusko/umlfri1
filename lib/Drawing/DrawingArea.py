import thread
import gobject
from lib.Base import CBaseObject
from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand
from lib.Drawing import CDiagram, CConnection, CElement, CConLabelInfo
from lib.Gui.common import CGuiObject


class CDrawingArea(CGuiObject):

    def __init__(self, app, diagram):
        CGuiObject.__init__(self, app)

        # CDiagram(None,_("Start page"))
        self.diagram = diagram
        self.paintlock = thread.allocate()
        self.toBePainted = False
        self.paintChanged = False

    def GetDiagram(self):
        '''
        Returns associated diagram.

        @return: Associated diagram
        @rtype:  L{Diagram<Diagram>}
        '''
        return self.diagram

    def ToPaint(self, changed = True):
        try:
            self.paintlock.acquire()
            self.paintChanged = self.paintChanged or changed
            if not self.toBePainted:
                self.toBePainted = True
                gobject.timeout_add(15, self.Paint)
        finally:
            self.paintlock.release()

    def Paint(self, canvas):
        '''
        Paints diagram at canvas

        @param canvas: Canvas on which its being drawn
        @type  canvas: L{CCairoCanvas<lib.Drawing.Canvas.CairoCanvas.CCairoCanvas>}
        '''


    def Paint(self, changed = True):

        if self.disablePaint:
            return
        try:
            self.paintlock.acquire()
            self.toBePainted = False
            changed = changed or self.paintChanged
            self.paintChanged = False
        finally:
            self.paintlock.release()

        self.diagram.Paint(self.canvas)

    def ShiftElements(self, actionName):
        if (actionName == 'SendBack'):
            self.Diagram.ShiftElementsBack()
        elif (actionName == 'BringForward'):
            self.Diagram.ShiftElementsForward()
        elif (actionName == 'ToBottom'):
            self.Diagram.ShiftElementsToBottom()
        elif (actionName == 'ToTop'):
            self.Diagram.ShiftElementsToTop()
        self.Paint()

    def CopySelectedObjects(self):
        self.Diagram.CopySelection(self.application.GetClipboard())

    def CutSelectedObjects(self):
        self.Diagram.CutSelection(self.application.GetClipboard())
        self.Paint()
        self.emit('selected-item', list(self.Diagram.GetSelected()),False)

    def PasteObjects(self):
        self.Diagram.PasteSelection(self.application.GetClipboard())
        self.Paint()
        self.emit('selected-item', list(self.Diagram.GetSelected()),False)

    def DuplicateSelectedObjects(self):
        cmd  = CDuplicateElementsCommand(tuple(self.Diagram.GetSelectedElements()), self.Diagram)
        self.application.GetCommands().Execute(cmd)
        self.Paint()

    def ShiftDeleteSelectedObjects(self):
        for sel in self.Diagram.GetSelected():
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
        self.Diagram.SpaceElementsEvenlyXY(isHorizontal)
        self.Paint()

    def PaintSelected(self, canvas):
        self.diagram.PaintSelected(canvas)
