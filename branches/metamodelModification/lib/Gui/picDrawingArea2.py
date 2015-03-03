from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
from lib.Drawing.DrawingArea import CDrawingArea

from lib.consts import BUFFER_SIZE, PROJECT_NODE_UID_SELECTION_TARGET
from lib.Distconfig import IMAGES_PATH

from common import CWidget, event
from lib.Drawing import CDiagram, CElement, CConnection
from lib.Drawing.DrawingAreaMouseDownEventArgs import CDrawingAreaMouseDownEventArgs
from lib.Drawing.DrawingAreaMouseUpEventArgs import CDrawingAreaMouseUpEventArgs
from lib.Drawing.DrawingAreaKeyPressEventArgs import CDrawingAreaKeyPressEventArgs
from lib.Drawing.DrawingAreaKeyUpEventArgs import CDrawingAreaKeyUpEventArgs
from lib.Drawing.DrawingAreaScrollEventArgs import CDrawingAreaScrollEventArgs

from lib.Drawing.Canvas import CCairoCanvas

import thread
import os.path


targets = [('document/uml', 0, gtk.TARGET_SAME_WIDGET)]

class Record(object): pass

class CpicDrawingArea(CWidget):
    name = 'picDrawingArea'
    widgets = ('picDrawingArea', 'picEventBox', 'picVBar', 'picHBar',
            'pMenuShift',
                'mnuCtxCut',
                'mnuCtxCopy',
                'mnuCtxPaste',
                'mnuCtxDuplicate',
                'mnuCtxDelete',
                'mnuCtxShiftDelete',
                'pmShowInProjectView',
                'mnuChangeSourceTarget',

                    'pmShift_SendBack',
                    'pmShift_BringForward',
                    'pmShift_ToBottom',
                    'pmShift_ToTop',
                'mnuAlign',
                    'mnuAlignLeftMost', 'mnuAlignLeftCurrent',
                    'mnuAlignRightMost', 'mnuAlignRightCurrent',
                    'mnuAlignUpwardsMost', 'mnuAlignUpwardsCurrent',
                    'mnuAlignDownwardsMost', 'mnuAlignDownwardsCurrent',
                    'mnuAlignCenterHor',
                    'mnuAlignCenterVer',
                'mnuSpacing',
                    'mnuSpaceEvenlyHorizontally',
                    'mnuSpaceEvenlyVertically',
                'mnuSizing',
                    'mnuResizeByMaximalElement',
                    'mnuResizeByMinimalElement',
                'mnuSnapSelectGrid',
                'pmOpenSpecification',
                'mnuResizeHight',
                'mnuResizeWidth',
                'mnuResizeHightAndWidth',)

    __gsignals__ = {
    }

    def __init__(self, app, wTree):
        self.paintlock = thread.allocate()
        self.toBePainted = False
        self.paintChanged = False
        self.canvas = None
        CWidget.__init__(self, app, wTree)
        self.__invalidated = False
        self.pressedKeys = set()
        self.buffer_size = ((0, 0), BUFFER_SIZE)
        self.diagrams = dict()
        self.activeDiagram = None
        self.activeDrawingArea = None
        self.picDrawingArea.realize()
        self.buffer = gtk.gdk.Pixmap(self.picDrawingArea.window, *self.buffer_size[1])
        self.SetDiagram(CDiagram(None,_("Start page")))

        self.TARGETS = [
        (PROJECT_NODE_UID_SELECTION_TARGET, 0, 0),
        ('text/plain', 0, 1),
        ('TEXT', 0, 2),
        ('STRING', 0, 3),
        ]

        self.picEventBox.drag_dest_set(gtk.DEST_DEFAULT_ALL, self.TARGETS, gtk.gdk.ACTION_COPY)
        self.AdjustScrollBars()
        self.cursorImages = {None: None}
        self.__invalidated = False

    def __OpenSpecification(self, obj):
        frmProps = self.application.GetWindow('frmProperties')
        frmProps.SetParent(self.application.GetWindow('frmMain'))
        frmProps.ShowPropertiesWindow(obj, self.application)

    def __UpdateCursor(self):
        """
        Updates current cursor from active L{CDrawingArea<lib.Drawing.DrawingArea>}. Loads cursor image, if necessary.
        """
        cursorFile = self.activeDrawingArea.GetCursorFile()
        cursorImage = self.cursorImages.get(cursorFile)
        if cursorImage is None and cursorFile is not None:
            cursorImage = gtk.gdk.Cursor(
                    gtk.gdk.display_get_default(),
                    gtk.gdk.pixbuf_new_from_file(os.path.join(IMAGES_PATH, cursorFile)),
                    0,
                    0
                )
            self.cursorImages[cursorFile] = cursorImage

        self.__SetCursor(cursorImage)

    def __SetCursor(self, cursorImage = None):
        """
        Sets cursor to specified image

        @param cursorImage: Cursor image to set cursor to.
        @type cursorImage: L{Cursor<gtk.gdk.Cursor>}
        """
        self.picDrawingArea.window.set_cursor(cursorImage)

    def BestFitScale(self):
        self.activeDrawingArea.BestFitScale()
        self.__OnScaleChanged()

    def IncreaseScale(self):
        self.activeDrawingArea.IncreaseScale()
        self.__OnScaleChanged()

    def DecreaseScale(self):
        self.activeDrawingArea.DecreaseScale()
        self.__OnScaleChanged()

    def __OnScaleChanged(self):
        self.__UpdateScrollBarsPosition()
        self.Paint()

    def GetScale(self):
        return self.activeDrawingArea.GetScale()

    def CanIncreaseScale(self):
        return self.activeDrawingArea.CanIncreaseScale()

    def CanDecreaseScale(self):
        return self.activeDrawingArea.CanDecreaseScale()

    def SetNormalScale(self):
        self.activeDrawingArea.SetScale(1.0)
        self.__UpdateScrollBarsPosition()
        self.Paint()

    def Redraw(self):
        self.canvas = CCairoCanvas(self.picDrawingArea, self.buffer, self.application.GetProject().GetMetamodel().GetStorage())

    def GetDiagram(self):
        return self.activeDiagram

    def SetDiagram(self, diagram):
        self.__SetActiveDiagram(diagram)

        self.__UpdateViewPortForDrawingArea(self.activeDrawingArea)
        self.Paint()

    def GetWindowSize(self):
        window = self.picDrawingArea.window
        if window is None:
            return (None, None)
        x, y =  window.get_size()
        return (x, y)

    def __UpdateViewPortForDrawingArea(self, drawingArea):
        """
        Updates drawing area's view port size, if the window size is available

        @param drawingArea: L{CDrawingArea<lib.Drawing.CDrawingArea>}
        @return:
        """
        windowSize = self.GetWindowSize()
        if windowSize == (None, None):
            return

        drawingArea.SetPhysicalViewPortSize(windowSize)

    def ViewPortChanged(self):
        """
        Called, when view port has changed. Informs DrawingArea of the new view port bounds.

        @rtype: bool
        @return: True, if drawing area needs to be resized, False if not.
        """
        drawingArea = self.activeDrawingArea
        if drawingArea is None:
            return

        viewPort = self.GetCurrentViewPort()
        if viewPort is None:
            return

        return drawingArea.SetPhysicalViewPort(viewPort)

    def GetCurrentViewPort(self):
        """
        Returns current visible view port.

        @rtype: tuple
        @return: Current view port (tuple: (x, y), (w, h))
        """
        x, y = int(self.picHBar.get_value()), int(self.picVBar.get_value())
        size = self.GetWindowSize()
        if size == (None, None):
            return None

        viewPort = (x, y), size

        return viewPort

    def SetScrollBarsPosition(self, pos = (0, 0)):
        self.AdjustScrollBars()

        # setting scrollbars' positions need to be done atomically

        self.picVBar.handler_block_by_func(self.on_picVBar_value_changed)
        self.picHBar.handler_block_by_func(self.on_picHBar_value_changed)
        self.picHBar.set_value(pos[0])
        self.picVBar.set_value(pos[1])
        self.picVBar.handler_unblock_by_func(self.on_picVBar_value_changed)
        self.picHBar.handler_unblock_by_func(self.on_picHBar_value_changed)

    def GetAbsolutePos(self, (posx, posy)):
        #((bposx, bposy), (bsizx, bsizy)) = self.buffer_size
        x,y = self.canvas.ToLogical((posx,posy))
        h,v = self.canvas.ToLogical((self.picHBar.get_value(),self.picVBar.get_value()))
        return int(x+h), int(y+v)

    def ToPaint(self, changed = True):
        try:
            self.paintlock.acquire()
            self.paintChanged = self.paintChanged or changed
            if not self.toBePainted:
                self.toBePainted = True
                gobject.timeout_add(15, self.Paint)
        finally:
            self.paintlock.release()


    def Paint(self, changed = True):
        if not self.picDrawingArea.window or not self.canvas:
            if changed:
                self.__invalidated = True # redraw completly on next configure event
            return

        try:
            self.paintlock.acquire()
            self.toBePainted = False
            changed = changed or self.paintChanged
            self.paintChanged = False
        finally:
            self.paintlock.release()


        # After the first time drawing area is shown, it reports wrong size
        # We need to check, if it has changed and update drawing area's view port size, if necessary

        if self.activeDrawingArea.GetPhysicalViewPortSize() != self.GetWindowSize():
            self.__UpdateViewPortForDrawingArea(self.activeDrawingArea)

        self.activeDrawingArea.Paint(self.canvas, changed)

        self.AdjustScrollBars()

        wgt = self.picDrawingArea.window
        gc = wgt.new_gc()

        pos = self.activeDrawingArea.GetPhysicalViewPortPos()
        size = self.activeDrawingArea.GetPhysicalViewPortSize()

        # when virtual drawing area is repositioned (due to view port getting out of the area's bounds)
        # the "drawing origin" (0, 0) is moved and we can't simply draw buffer on position offseted by view port position

        # it's because draw_drawable() second and third arguments are offsets within source drawable
        # but after the drawing origin is moved, diagram's elements are offseted (using delta parameter)
        # and when we offset the buffer, the elements are moved even further (in opposite direction of the scrolling)

        drawPosition = self.activeDrawingArea.OffsetOnVirtualArea(pos)
        wgt.draw_drawable(gc, self.buffer, drawPosition[0], drawPosition[1], 0, 0, size[0], size[1])

    def AdjustScrollBars(self):
        dasx, dasy = self.activeDrawingArea.GetDiagramPhysicalSize()

        wisx, wisy = self.GetWindowSize()
        tmp = self.picHBar.get_adjustment()
        tmp.upper = dasx
        tmp.page_size = wisx
        self.picHBar.set_adjustment(tmp)

        tmp = self.picVBar.get_adjustment()
        tmp.upper = dasy
        tmp.page_size = wisy
        self.picVBar.set_adjustment(tmp)

    @event("mnuCtxDelete","activate")
    def DeleteElements(self, widget = None):
        self.activeDrawingArea.DeleteSelectedObjects()
        self.Paint()

    def UpdateMenuSensitivity(self, project, diagram, element, topElement, connection):
        self.pmShowInProjectView.set_sensitive(element)
        for item in self.pMenuShift.get_children():
            item.set_sensitive(element)

        self.mnuCtxPaste.set_sensitive(
            diagram and not self.application.GetClipboard().IsEmpty()
            and not bool(set(i.GetObject() for i in self.activeDiagram.GetElements()).intersection(set(i.GetObject() for i in self.application.GetClipboard().GetContent())))
        )

        selection = list(self.activeDiagram.GetSelection().GetSelectedSet())
        self.pmOpenSpecification.set_sensitive(len(selection) <= 1)
        self.mnuChangeSourceTarget.set_sensitive(connection and len(selection) == 1)
        self.mnuAlign.set_sensitive(element)
        self.mnuSpacing.set_sensitive(element)
        self.mnuSizing.set_sensitive(element)
        self.mnuSnapSelectGrid.set_sensitive(element)
        self.mnuCtxCopy.set_sensitive(element)
        self.mnuCtxCut.set_sensitive(element)
        self.mnuCtxDuplicate.set_sensitive(element)
        self.mnuCtxDelete.set_sensitive(connection or element)

        self.mnuCtxShiftDelete.set_sensitive((connection or element) and not topElement)

    @event('application.bus', 'position-change', False)
    @event('application.bus', 'position-change-from-plugin', True)
    @event('application.bus', 'many-position-change', False)
    def ElementPositionChange(self, widget, elements, plugin):
        if plugin:
            self.activeDrawingArea.ToPaint()
        else:
            self.activeDrawingArea.Paint()

    @event('application.bus', 'selected-toolbox-item-changed')
    def on_toolbox_item_selected(self, widget, item):
        self.activeDrawingArea.OnToolBoxItemSelected(item)

    @event('application.bus', 'properties-editing-started')
    def on_properties_editing_started (self, widget):
        self.pMenuShift.set_sensitive (False)

    @event('application.bus', 'properties-editing-stoped')
    def on_properties_editing_ended (self, widget):
        self.pMenuShift.set_sensitive (True)

    @event("picEventBox", "button-press-event")
    def on_picEventBox_button_press_event(self, widget, event):
        self.picDrawingArea.grab_focus()
        pos = (event.x, event.y)

        isDoubleClick = event.type == gtk.gdk._2BUTTON_PRESS
        wasSpacePressed = gtk.keysyms.space in self.pressedKeys

        eventArgs = CDrawingAreaMouseDownEventArgs(pos, event.button, isDoubleClick, wasSpacePressed, event.state)

        self.activeDrawingArea.OnMouseDown(eventArgs)
        self.__UpdateCursor()

        self.Paint()

        if event.button == 3:
            #if something is selected:
            #self.UpdateMenuSensitivity(bool(self.application.GetProject()), bool(self.activeDiagram), int(len(list(self.activeDiagram.GetSelection().GetSelected())) > 0))
            self.pMenuShift.popup(None,None,None,event.button,event.time)
            return True

    @event("picEventBox", "button-release-event")
    def on_button_release_event(self, widget, event):
        pos = (event.x, event.y)

        wasSpacePressed = gtk.keysyms.space in self.pressedKeys

        eventArgs = CDrawingAreaMouseUpEventArgs(pos, event.button, wasSpacePressed, event.state)

        self.activeDrawingArea.OnMouseUp(eventArgs)
        self.__UpdateCursor()
        self.AdjustScrollBars()
        self.Paint()

    @event("picEventBox", "key-press-event")
    def on_key_press_event(self, widget, event):
        if (event.keyval in self.pressedKeys and
            event.keyval not in (gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Up, gtk.keysyms.Down)):
            return True

        self.pressedKeys.add(event.keyval)

        eventArgs = CDrawingAreaKeyPressEventArgs(self.pressedKeys, event.state)

        self.activeDrawingArea.OnKeyPress(eventArgs)

        self.__UpdateCursor()
        self.__UpdateScrollBarsPosition()
        self.Paint()

        return True

    @event("picEventBox", "key-release-event")
    def on_key_release_event(self, widget, event):

        self.pressedKeys.discard(event.keyval)

        eventArgs = CDrawingAreaKeyUpEventArgs(self.pressedKeys, event.keyval, event.state)

        self.activeDrawingArea.OnKeyUp(eventArgs)

        self.__UpdateCursor()
        self.__UpdateScrollBarsPosition()
        self.Paint()

    @event("picEventBox", "motion-notify-event")
    def on_motion_notify_event(self, widget, event):
        pos = (event.x, event.y)
        self.activeDrawingArea.OnMouseMove(pos)
        self.__UpdateScrollBarsPosition()
        self.Paint()

    @event("picEventBox","drag-data-received")
    def on_drag_data_received(self, widget, drag_context, x, y, selection, targettype, timestamp):
        uid = selection.data
        self.activeDrawingArea.DropElementFromProjectTree(uid, (x, y))
        self.Paint()

    @event("picDrawingArea", "configure-event")
    @event("picDrawingArea", "expose-event")
    @event("picDrawingArea", "size-allocate")
    def on_picDrawingArea_expose_event(self, widget, tmp):
        inv = self.__invalidated
        self.__invalidated = False
        self.Paint(inv)

    @event("picVBar", "value-changed")
    def on_picVBar_value_changed(self, widget):
        changed = self.ViewPortChanged()
        self.Paint(changed)

    @event("picHBar", "value-changed")
    def on_picHBar_value_changed(self, widget):
        changed = self.ViewPortChanged()
        self.Paint(changed)

    @event("picEventBox", "scroll-event")
    def on_picEventBox_scroll_event(self, widget, event):
        eventArgs = CDrawingAreaScrollEventArgs(event.direction, event.state)

        changed = self.activeDrawingArea.OnScroll(eventArgs)
        self.__UpdateScrollBarsPosition()
        self.Paint(changed)

    @event("picDrawingArea", "focus-out-event")
    def on_picDrawingArea_focus_out_event(self, widget, event):
        self.activeDrawingArea.OnLostFocus()

    def __AddDiagram(self, diagram):
        drawing_area = CDrawingArea(self.application, diagram)
        self.diagrams[diagram] = drawing_area

    def __SetActiveDiagram(self, diagram):
        if self.diagrams.has_key(diagram) == False:
            self.__AddDiagram(diagram)
        self.activeDiagram = diagram
        self.activeDrawingArea = self.diagrams[diagram]
        return self.activeDrawingArea

    def SetFocus(self):
        self.picDrawingArea.grab_focus()

    @event("pmShowInProjectView","activate")
    def on_mnuShowInProjectView_click(self, menuItem):
        self.activeDrawingArea.ShowSelectedObjectInProjectView()

    @event("pmOpenSpecification","activate")
    def on_mnuOpenSpecification_click(self, menuItem):
        self.activeDrawingArea.OpenSpecificationForSelectedObject()

    @event("pmShift_SendBack","activate","SendBack")
    @event("pmShift_BringForward","activate","BringForward")
    @event("pmShift_ToBottom","activate","ToBottom")
    @event("pmShift_ToTop","activate", "ToTop")
    def on_pmShift_SendBack_activate(self, menuItem, actionName):
        self.activeDrawingArea.ShiftElements(actionName)
        self.Paint()

    @event("mnuCtxCopy","activate")
    def ActionCopy(self, widget = None):
        self.activeDrawingArea.CopySelectedObjects()
        self.Paint()

    @event("mnuCtxCut", "activate")
    def ActionCut(self, widget = None):
        self.activeDrawingArea.CutSelectedObjects()
        self.Paint()

    @event("mnuCtxPaste","activate")
    def ActionPaste(self, widget = None):
        self.activeDrawingArea.PasteObjects()
        self.Paint()

    @event("mnuCtxDuplicate", "activate")
    def ActionDuplicate(self, widget=None):
        self.activeDrawingArea.DuplicateSelectedObjects()
        self.Paint()

    @event("mnuCtxShiftDelete","activate")
    def onMnuCtxShiftDelteActivate(self, menuItem):
        self.activeDrawingArea.ShiftDeleteSelectedObjects()
        self.Paint()

    @event("mnuChangeSourceTarget","activate")
    def on_mnuChangeSourceTarget_click(self,widget):
        self.activeDrawingArea.ChangeConnectionSourceTarget()
        self.Paint()

    @event("mnuAlignLeftMost","activate", True, True, False)
    @event("mnuAlignLeftCurrent","activate", True, True, True)
    @event("mnuAlignRightMost","activate", True, False, False)
    @event("mnuAlignRightCurrent","activate", True, False, True)
    @event("mnuAlignUpwardsMost","activate", False, True, False)
    @event("mnuAlignUpwardsCurrent","activate", False, True, True)
    @event("mnuAlignDownwardsMost","activate", False, False, False)
    @event("mnuAlignDownwardsCurrent","activate", False, False, True)
    def on_mnuAlign_activate(self, menuItem, horiz, lower, defaultE):
        self.activeDrawingArea.Align(horiz, lower, defaultE)
        self.Paint()

    @event("mnuAlignCenterHor","activate", True, True)
    @event("mnuAlignCenterVer","activate", False, True)
    def on_mnuAlignCenter(self, widget, isHorizontal, alignToSelectedElement):
        self.activeDrawingArea.AlignCenter(isHorizontal, alignToSelectedElement)
        self.Paint()

    @event("mnuResizeHight","activate")
    def on_mnuResizeHight(self, menuItem):
        self.activeDrawingArea.ResizeHeight()
        self.Paint()

    @event("mnuResizeWidth","activate")
    def on_mnuResizeWidth(self, menuItem):
        self.activeDrawingArea.ResizeWidth()
        self.Paint()

    @event("mnuResizeHightAndWidth","activate")
    def on_mnuResizeWidthAndHight(self, menuItem):
        self.activeDrawingArea.ResizeWidthAndHeight()
        self.Paint()

    @event("mnuResizeByMaximalElement","activate")
    def on_mnuResizeByMaximalElement(self, menuItem):
        self.activeDrawingArea.ResizeByMaximalElement()
        self.Paint()

    @event("mnuResizeByMinimalElement","activate")
    def on_mnuResizeByMinimalElement(self, menuItem):
        self.activeDrawingArea.ResizeByMinimalElement()
        self.Paint()

    @event("mnuSpaceEvenlyHorizontally","activate", True)
    @event("mnuSpaceEvenlyVertically","activate", False)
    def on_mnuMakeSpacing(self, widget, isHorizontal):
        self.activeDrawingArea.MakeSpacing(isHorizontal)
        self.Paint()

    @event('mnuSnapSelectGrid', 'activate')
    def on_mnuSnapSelected(self, widget):
        self.activeDrawingArea.SnapSelected()
        self.Paint()

    def HasFocus(self):
        return self.picDrawingArea.is_focus()

    def Export(self, filename, export_type, zoom, padding, background=None):
        self.activeDrawingArea.Export(filename, export_type, zoom, padding, background)
        self.Paint()

    def GetSelectionPixbuf(self, zoom, padding, background):
        return self.activeDrawingArea.GetSelectionPixbuf(zoom, padding, background)

    def SelectObject(self, object):
        self.activeDrawingArea.SelectObject(object)
        self.AdjustScrollBars()
        self.Paint()

    def __UpdateScrollBarsPosition(self):
        self.SetScrollBarsPosition(self.activeDrawingArea.GetPhysicalViewPortPos())

    def DeselectAll(self):
        self.activeDrawingArea.DeselectAll()

    @event('application.bus', 'connection-changed')
    @event('application.bus', 'element-changed')
    def ObjectChanged(self, bus, params):
        self.ToPaint()