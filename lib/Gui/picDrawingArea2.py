from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand
from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
from lib.Drawing.DrawingArea import CDrawingArea

from lib.Project import CProject, CProjectNode

from lib.consts import BUFFER_SIZE, SCALE_MIN, SCALE_MAX, SCALE_INCREASE
from lib.config import config
from lib.Distconfig import IMAGES_PATH

from common import CWidget, event
from lib.Drawing import CDiagram, CElement, CConnection, CConLabelInfo
from lib.Drawing.DrawingAreaMouseDownEventArgs import CDrawingAreaMouseDownEventArgs
from lib.Drawing.DrawingAreaMouseUpEventArgs import CDrawingAreaMouseUpEventArgs
from lib.Drawing.DrawingAreaKeyPressEventArgs import CDrawingAreaKeyPressEventArgs
from lib.Drawing.DrawingAreaKeyUpEventArgs import CDrawingAreaKeyUpEventArgs

from lib.Elements import CElementObject
from lib.Connections import CConnectionObject
from lib.Exceptions.UserException import *
from lib.Drawing.Canvas import CCairoCanvas, CExportCanvas
from lib.Drawing import Element

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
        'get-selected':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT,
            ()),
        'set-selected':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT, )),
        'drop-from-treeview': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
        'show-element-in-treeView': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    }

    def __init__(self, app, wTree):
        self.setResize = True
        self.adjScrollbars = ""
        self.getPlusMove = 0
        self.disablePaint = False
        self.paintlock = thread.allocate()
        self.tobePainted = False
        self.paintChanged = False
        self.canvas = None
        CWidget.__init__(self, app, wTree)
        self.keydragPosition = None
        self.__invalidated = False
        self.__NewConnection = None
        self.dnd = None
        self.selecting = None
        self.selElem = None
        self.selSq = None
        self.pressedKeys = set()
        self.scale = 1.0
        self.buffer_size = ((0, 0), BUFFER_SIZE)
        self.diagrams = dict()
        self.activeDiagram = None
        self.activeDrawingArea = None
        self.picDrawingArea.realize()
        self.buffer = gtk.gdk.Pixmap(self.picDrawingArea.window, *self.buffer_size[1])
        self.SetDiagram(CDiagram(None,_("Start page")))
        cmap = self.picDrawingArea.window.get_colormap()
        self.DragGC = self.picDrawingArea.window.new_gc(foreground = cmap.alloc_color(str(config['/Styles/Drag/RectangleColor'].Invert())),
            function = gtk.gdk.XOR, line_width = config['/Styles/Drag/RectangleWidth'])

        self.TARGETS = [
        ('MY_TREE_MODEL_ROW', gtk.TARGET_SAME_WIDGET, 0),
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
        winSizeX, winSizeY = self.GetWindowSize()
        (diaSizeMinX, diaSizeMinY), (diaSizeMaxX, diaSizeMaxY) = self.Diagram.GetSizeSquare()
        scaleX = float(winSizeX) / float(diaSizeMaxX-diaSizeMinX)
        scaleY = float(winSizeY) / float(diaSizeMaxY-diaSizeMinY)
        if scaleX > scaleY :
            scale = scaleY
        else : scale = scaleX
        
        if scale < SCALE_MIN:
            scale = SCALE_MIN
        elif scale > SCALE_MAX:
            scale = SCALE_MAX

        self.SetScale(scale)
        diaSizeMinX, diaSizeMinY = self.canvas.ToPhysical((diaSizeMinX, diaSizeMinY))
        self.picHBar.set_value(diaSizeMinX)
        self.picVBar.set_value(diaSizeMinY)

    def IncScale(self, scale):
        self.activeDrawingArea.IncScale(scale)
        self.__UpdateScrollBarsPosition()
        self.Paint()

    def ShiftScrollbars(self, direction):
        posx,posy = self.GetPos()
        if(self.getPlusMove > 0):
            move = int(self.getPlusMove / 2)
        else:
            move = 5
        if(direction == "right"):
            self.SetScrollBarsPosition((posx + move, posy))
        if(direction == "left"):
            self.SetScrollBarsPosition((posx - move, posy))
        if(direction == "up"):
            self.SetScrollBarsPosition((posx, posy+move))
        if(direction == "down"):
            self.SetScrollBarsPosition((posx, posy-move))
        self.setResize = False
        self.getPlusMove = 0

    def GetDirection(self, direction):
        self.adjScrollbars = direction

    def GetPlusMove(self, plusmove):
        self.getPlusMove = plusmove

    def PlusMove(self, horVer):
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
            
    def GetScale(self):
        return self.canvas.GetScale()
    
    def SetNormalScale(self):
        self.picHBar.set_value(0)
        self.picVBar.set_value(0)
        self.SetScale(1.0)
            
    def Redraw(self):
        self.canvas = CCairoCanvas(self.picDrawingArea, self.buffer, self.application.GetProject().GetMetamodel().GetStorage())
        self.canvas.SetScale(self.scale)

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

        drawingArea.SetViewPortSize(windowSize)

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

        return drawingArea.SetViewPort(viewPort)

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

    def GetDiagramSize(self):
        tmp = [int(max(i)) for i in zip(self.activeDiagram.GetSize(), self.picDrawingArea.window.get_size())]
        return tuple(tmp)
    
    def GetPos(self):
        return int(self.picHBar.get_value()), int(self.picVBar.get_value())
        
    def SetScrollBarsPosition(self, pos = (0, 0)):
        self.picHBar.set_value(pos[0])        
        self.picVBar.set_value(pos[1])

    def GetAbsolutePos(self, (posx, posy)):
        #((bposx, bposy), (bsizx, bsizy)) = self.buffer_size
        x,y = self.canvas.ToLogical((posx,posy))
        h,v = self.canvas.ToLogical((self.picHBar.get_value(),self.picVBar.get_value()))
        return int(x+h), int(y+v)

    def GetRelativePos(self, (posx, posy)):
        x,y = self.canvas.ToPhysical((posx,posy))
        h,v = (self.picHBar.get_value(),self.picVBar.get_value())
        return int(-h+x), int(-v+y)

    def ToPaint(self, changed = True):
        try:
            self.paintlock.acquire()
            self.paintChanged = self.paintChanged or changed
            if not self.tobePainted:
                self.tobePainted = True
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

        if self.activeDrawingArea.GetViewPortSize() != self.GetWindowSize():
            self.__UpdateViewPortForDrawingArea(self.activeDrawingArea)

        self.activeDrawingArea.Paint(self.canvas, changed)

        self.AdjustScrollBars()
        wgt = self.picDrawingArea.window
        gc = wgt.new_gc()

        pos = self.activeDrawingArea.GetViewPortPos()
        size = self.activeDrawingArea.GetViewPortSize()

        # wgt.draw_drawable(gc, self.buffer, posx - bposx, posy - bposy, 0, 0, sizx, sizy)
        wgt.draw_drawable(gc, self.buffer, pos[0], pos[1], 0, 0, size[0], size[1])

        # if(self.adjScrollbars != ""):
        #     self.ShiftScrollbars(self.adjScrollbars)
        #     self.adjScrollbars = ""
        #
        # if self.dnd == 'resize':
        #     self.__DrawResRect((None, None), True, False)
        # elif self.dnd == 'rect':
        #     self.__DrawDragRect((None, None), True, False)
        # elif self.dnd == 'point':
        #     self.__DrawDragPoint((None, None), True, False)
        # elif self.dnd == 'selection':
        #     self.__DrawDragSel((None, None), True, False)
        # if self.__NewConnection is not None:
        #     self.__DrawNewConnection((None, None), False)

    def AdjustScrollBars(self):
        if self.canvas is None:
            dasx, dasy = self.GetDiagramSize()
        else : 
            #dasx, dasy = self.GetDiagramSize()
            dasx, dasy = self.canvas.ToPhysical(self.GetDiagramSize())
                
        wisx, wisy = self.GetWindowSize()
        tmp = self.picHBar.get_adjustment()
        tmp.upper = dasx
        tmp.page_size = wisx
        self.picHBar.set_adjustment(tmp)

        tmp = self.picVBar.get_adjustment()
        tmp.upper = dasy
        tmp.page_size = wisy
        self.picVBar.set_adjustment(tmp)

    def Export(self, filename, export_type, zoom, padding, background=None):
        self.Diagram.DeselectAll()
        
        (x1, y1), (x2, y2) = self.Diagram.GetSizeSquare()
        sizeX = x2 - x1
        sizeY = y2 - y1
        x = x1
        y = y1

        sizeX = (sizeX + padding*2) * zoom
        sizeY = (sizeY + padding*2) * zoom
        canvas = CExportCanvas(self.application.GetProject().GetMetamodel().GetStorage(), export_type,
            filename, sizeX, sizeY, background = background)
        canvas.SetScale(zoom)
        canvas.MoveBase(x - padding, y - padding)
        self.Diagram.PaintFull(canvas)
        canvas.Finish()
        self.Paint()
    
    @event("mnuCtxDelete","activate")
    def DeleteElements(self, widget = None):
        self.drawingArea.DeleteSelectedObjects()
    
    def UpdateMenuSensitivity(self, project, diagram, element, topElement, connection):
        self.pmShowInProjectView.set_sensitive(element)
        for item in self.pMenuShift.get_children():
            item.set_sensitive(element)
            
        self.mnuCtxPaste.set_sensitive(
            diagram and not self.application.GetClipboard().IsEmpty()
            and not bool(set(i.GetObject() for i in self.Diagram.GetElements()).intersection(set(i.GetObject() for i in self.application.GetClipboard().GetContent())))
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
            self.drawingArea.ToPaint()
        else:
            self.drawingArea.Paint()

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
            #self.UpdateMenuSensitivity(bool(self.application.GetProject()), bool(self.Diagram), int(len(list(self.Diagram.GetSelected())) > 0))
            self.pMenuShift.popup(None,None,None,event.button,event.time)
            return True

    def __AddItem(self, toolBtnSel, event):
        pos = self.GetAbsolutePos((event.x, event.y))
        if toolBtnSel[0] == 'Element':
            ElementType = self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(toolBtnSel[1])
            ElementObject = CElementObject(ElementType)
            newElement = CElement(self.Diagram, ElementObject)
            newElement.SetPosition(pos)
            self.Diagram.MoveElement(newElement, pos)
            self.AdjustScrollBars()
            self.emit('set-selected', None)
            #here, I get prent element of selected elements (if element is on (over) another element)
            minzorder = 9999999
            parentElement = None
            for el in self.Diagram.GetSelectedElements(True):
                pos1, pos2 = el.GetSquare()
                zorder = self.Diagram.GetElementZOrder(el)
                if newElement.AreYouInRange(pos1, pos2, True):
                    for el2 in self.Diagram.GetElementsInRange(pos1, pos2, True):
                        if self.Diagram.GetElementZOrder(el2) < minzorder:        #get element with minimal zorder
                            minzorder = self.Diagram.GetElementZOrder(el2)
                            parentElement = el2.GetObject()
                    
            self.Diagram.DeselectAll()
            self.application.GetBus().emit('add-element', ElementObject, self.Diagram, parentElement)
            self.Diagram.AddToSelection(newElement)
            self.emit('selected-item', list(self.Diagram.GetSelected()),True)
            self.Paint()

        elif toolBtnSel[0] == 'Connection':
            itemSel = self.Diagram.GetElementAtPosition(pos)

            if itemSel is None:
                if self.__NewConnection is not None:
                    pass
            elif isinstance(itemSel, (CConnection, CConLabelInfo)):
                return
            elif self.__NewConnection is None:
                ConnectionType = self.application.GetProject().GetMetamodel().GetConnectionFactory().GetConnection(toolBtnSel[1])
                center = itemSel.GetCenter()
                relcenter = self.GetRelativePos(center)
                self.__NewConnection = (ConnectionType, [center], itemSel)
                self.__DrawNewConnection(relcenter, False)
            else:
                pass

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
        self.Paint()

        return

        if event.keyval==gtk.keysyms.a and event.state == gtk.gdk.CONTROL_MASK:
            self.Diagram.SelectAll()
            self.emit('selected-item', list(self.Diagram.GetSelected()),False)
            self.Paint()
        elif event.keyval == gtk.keysyms.Delete:
            if self.dnd:
                return
            if event.state == gtk.gdk.SHIFT_MASK:
                for sel in self.Diagram.GetSelected():
                    if isinstance(sel, Element.CElement):
                        self.emit('delete-element-from-all',sel.GetObject())
                    else:
                        self.Diagram.ShiftDeleteConnection(sel)
            else:
                for sel in self.Diagram.GetSelected():
                    self.Diagram.DeleteItem(sel)
                    self.emit('selected-item', list(self.Diagram.GetSelected()),False)
            self.Paint()
        elif event.keyval == gtk.keysyms.Escape:
            self.ResetAction()
            self.emit('set-selected', None)
        elif event.keyval == gtk.keysyms.space:
            self.__SetCursor('grab')
        
        elif event.keyval in (gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Up, gtk.keysyms.Down):
            selected = list(self.Diagram.GetSelectedElements())
            if selected:
                if self.dnd is None:
                    self.keydragPosition = list(selected[0].GetCenter())
                    e = Record()
                    e.x, e.y = self.keydragPosition
                    self.__BeginDragRect(e)
                if self.dnd == 'rect':
                    if self.keydragPosition is None:
                        self.keydragPosition = list(selected[0].GetCenter())
                    if gtk.keysyms.Right in self.pressedKeys:
                        self.keydragPosition[0] += 10 + self.PlusMove("hor")
                        self.GetDirection("right")
                        self.GetPlusMove((10 + self.PlusMove("hor")))
                    if gtk.keysyms.Left in self.pressedKeys:
                        self.keydragPosition[0] -= 10 + self.PlusMove("hor")
                        self.GetDirection("left")
                        self.GetPlusMove((10 + self.PlusMove("hor")))
                    if gtk.keysyms.Up in self.pressedKeys:
                        self.keydragPosition[1] -= 10 + self.PlusMove("ver")
                        self.GetDirection("down")
                        self.GetPlusMove((10 + self.PlusMove("ver")))
                    if gtk.keysyms.Down in self.pressedKeys:
                        self.keydragPosition[1] += 10 + self.PlusMove("ver")
                        self.GetDirection("up")
                        self.GetPlusMove((10 + self.PlusMove("ver")))
                    self.__DrawDragRect(self.keydragPosition)
        return True
    
    @event("picEventBox", "key-release-event")
    def on_key_release_event(self, widget, event):

        self.pressedKeys.discard(event.keyval)

        eventArgs = CDrawingAreaKeyUpEventArgs(self.pressedKeys, event.state)

        self.activeDrawingArea.OnKeyUp(eventArgs)

        self.__UpdateCursor()
        self.Paint()

        return

        if gtk.keysyms.space in self.pressedKeys:
            if self.dnd != 'move':
                self.__SetCursor(None)
        
        if (event.keyval in (gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Up, gtk.keysyms.Down) 
            and set() == self.pressedKeys.intersection(set([gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Up, gtk.keysyms.Down]))
            and self.dnd == 'rect'):
            
            delta = self.__GetDelta(self.keydragPosition)
            self.keydragPosition = None
            self.Diagram.MoveSelection(delta)
            self.dnd = None
            self.Paint()

    @event("picEventBox", "motion-notify-event")
    def on_motion_notify_event(self, widget, event):
        pos = (event.x, event.y)
        self.activeDrawingArea.OnMouseMove(pos)
        self.__UpdateScrollBarsPosition()
        self.Paint()
    
    @event("picEventBox","drag-data-received")
    def on_drag_data_received(self, widget, drag_context, x, y, selection, targettype, timestamp):
        position = self.GetAbsolutePos((x, y))
        self.emit('drop-from-treeview',position)
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
        if (event.state & gtk.gdk.CONTROL_MASK):
            if event.direction == gtk.gdk.SCROLL_UP:
                self.IncScale(SCALE_INCREASE)
                return
            elif event.direction == gtk.gdk.SCROLL_DOWN:
                self.IncScale(-SCALE_INCREASE)
                return           

        if  event.state & gtk.gdk.SHIFT_MASK :
            self.__Scroll(self.picHBar, event.direction)
        elif event.direction == gtk.gdk.SCROLL_LEFT:
            self.__Scroll(self.picHBar, event.direction)
        elif event.direction == gtk.gdk.SCROLL_RIGHT:
            self.__Scroll(self.picHBar, event.direction)
        else:
            self.__Scroll(self.picVBar, event.direction)
        self.Paint(False)

    @event("picDrawingArea", "focus-out-event")
    def on_picDrawingArea_foucus_out_event(self, widget, event):
        self.emit('set-selected', None)
        self.ResetAction()

    def __AddDiagram(self, diagram):
        drawing_area = CDrawingArea(self.application, diagram)
        self.diagrams[diagram] = drawing_area

    def __SetActiveDiagram(self, diagram):
        if self.diagrams.has_key(diagram) == False:
            self.__AddDiagram(diagram)
        self.activeDiagram = diagram
        self.activeDrawingArea = self.diagrams[diagram]
        return self.activeDrawingArea

    #TODO FIX: fix vertical scrolling
    def __Scroll(self, scrollbar, direction):
        tmp = scrollbar.get_adjustment()
        if direction == gtk.gdk.SCROLL_UP:
            tmp.value = max(tmp.lower, tmp.value - 20)
        elif direction == gtk.gdk.SCROLL_DOWN:
            tmp.value = min(tmp.upper - tmp.page_size, tmp.value + 20)
        elif direction == gtk.gdk.SCROLL_LEFT:
            tmp.value = max(tmp.lower, tmp.value - 20)
        elif direction == gtk.gdk.SCROLL_RIGHT:
            tmp.value = min(tmp.upper - tmp.page_size, tmp.value + 20)
        scrollbar.set_adjustment(tmp)

    def __BeginDragSel(self, event):
        self.DragSel = self.GetAbsolutePos((event.x, event.y))
        self.__DrawDragSel((event.x, event.y), False)
        self.dnd = 'selection'

    def __BeginDragRect(self, event):
        selElements = list(self.Diagram.GetSelectedElements())
        self.selElem = selElements[0]
        self.DragStartPos = self.GetAbsolutePos((event.x, event.y))
        if len(selElements) == 1:
            self.selSq = self.selElem.GetSquareAtPosition(self.DragStartPos)
            if(self.setResize == False):
                self.selSq = None
                self.setResize = True
        else:
            self.selSq = None
        
        self.DragRect = (self.Diagram.GetSelectSquare())
        self.DragPoint = list(self.DragRect[0])
        if (self.selSq is None): # Neresizujem
            self.__DrawDragRect((event.x, event.y), False)
            self.dnd = 'rect'
        else:
            self.__DrawResRect((event.x, event.y), False, True)
            for i in (0, 1):
                if self.selSq[i] > 0:
                    self.DragPoint[i] += self.DragRect[1][i]
            self.dnd = 'resize'

    def __BeginDragPoint(self, event, connection, point):
        self.DragStartPos = self.GetAbsolutePos((event.x, event.y))
        self.DragPoint = (connection, point)
        self.__DrawDragPoint((event.x, event.y), False)
        self.dnd = 'point'

    def __BeginDragLine(self, event, connection, point):
        self.DragStartPos = self.GetAbsolutePos((event.x, event.y))
        self.DragPoint = (connection, point)
        self.__DrawDragLine(event.x, event.y, False)
        self.dnd = 'line'
        
    def __BeginDragMove(self, event):
        self.__SetCursor('grabbing')
        self.DragStartPos = (event.x, event.y)
        self.Diagram.SetHScrollingPos(self.GetPos()[0])
        self.Diagram.SetVScrollingPos(self.GetPos()[1])
        self.dnd = 'move'
        
    def __GetDelta(self, pos, follow = False):
        if pos == (None, None):
            return 0, 0
        tmpx, tmpy = self.GetAbsolutePos(pos)
        dx, dy = tmpx - self.DragStartPos[0], tmpy - self.DragStartPos[1]
        posx, posy = self.DragPoint
        tmpx, tmpy = max(0, posx + dx), max(0, posy + dy)
        return int(tmpx - posx), int(tmpy - posy)

    def __DrawDragSel(self, pos, erase = True, draw = True):
        if erase:
            self.picDrawingArea.window.draw_rectangle(self.DragGC, False, *self.__oldsel)
        if draw:
            x1, y1 = self.DragSel
            x2, y2 = self.GetAbsolutePos(pos)
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            tmpx, tmpy = self.GetRelativePos((x1, y1))
            w, h = self.canvas.ToPhysical((x2 - x1, y2 - y1))
            if self.selSq is None:
                self.__oldsel = tmpx, tmpy, w, h
                self.picDrawingArea.window.draw_rectangle(self.DragGC, False, *self.__oldsel)

  
    def __DrawDragRect(self, pos, erase = True, draw = True):
        if erase:
            x1 = self.__oldpos[0]
            y1 = self.__oldpos[1]
            x2,y2 = self.canvas.ToPhysical(self.DragRect[1])
            self.picDrawingArea.window.draw_rectangle(self.DragGC, False, x1, y1, x2, y2)
        
        if draw:
            tmpx, tmpy = self.GetRelativePos(self.DragRect[0])
            dx, dy = self.__GetDelta(pos)
            if self.selSq is None:
                x1,y1 = self.canvas.ToPhysical((dx,dy))
                x1 = x1+ tmpx
                y1 = y1 + tmpy
                x2,y2 = self.canvas.ToPhysical(self.DragRect[1])
                self.picDrawingArea.window.draw_rectangle(self.DragGC, False, x1, y1, x2, y2)
                self.__oldpos = x1, y1

    def __DrawDragPoint(self, (x, y), erase = True, draw = True):
        if x is None:
            x, y = self.__oldPoints2
        connection, index = self.DragPoint
        prev, next = connection.GetNeighbours(index)
        abspos = self.GetAbsolutePos((x, y))
        x, y = max(abspos[0], 0), max(abspos[1], 0)
        x, y = self.GetRelativePos((x, y))
        points = [self.GetRelativePos(prev), (int(x), int(y)), self.GetRelativePos(next)]
        if erase:
            self.picDrawingArea.window.draw_lines(self.DragGC, self.__oldPoints)
        if draw:
            self.__oldPoints = points
            self.__oldPoints2 = self.GetAbsolutePos((x, y))
            self.picDrawingArea.window.draw_lines(self.DragGC, self.__oldPoints)

    def __DrawDragLine(self, x, y, erase = True, draw = True):
        if x is None:
            x, y = self.__oldPoints2
        abspos = self.GetAbsolutePos((x, y))
        x, y = max(abspos[0], 0), max(abspos[1], 0)
        x, y = self.GetRelativePos((x, y))
        connection, index = self.DragPoint
        all = tuple(connection.GetPoints())
        prev, next = all[index], all[index + 1]
        points = [self.GetRelativePos(prev), (int(x), int(y)), self.GetRelativePos(next)]
        if erase:
            self.picDrawingArea.window.draw_lines(self.DragGC, self.__oldPoints)
        if draw:
            self.__oldPoints = points
            self.__oldPoints2 = self.GetAbsolutePos((x, y))
            self.picDrawingArea.window.draw_lines(self.DragGC, self.__oldPoints)

    def __DrawDragMove(self, pos):
        posx, posy = self.Diagram.GetHScrollingPos(), self.Diagram.GetVScrollingPos()
        x1, y1 = pos
        x2, y2 = self.DragStartPos
        self.SetScrollBarsPosition((posx - x1 + x2, posy - y1 + y2))
        self.Paint(False)
        

    def __DrawNewConnection(self, (x, y), erase = True, draw = True):
        if x is None:
            points = self.__NewConnection[1][:]
        else:
            points = self.__NewConnection[1]
        points = [self.GetRelativePos(point) for point in points]
        if x is not None:
            points.append((int(x), int(y)))
        if erase:
            self.picDrawingArea.window.draw_lines(self.DragGC, self.__oldNewConnection)
        if draw:
            self.__oldNewConnection = points
            self.picDrawingArea.window.draw_lines(self.DragGC, self.__oldNewConnection)

    def ResetAction(self):
        self.dnd = None
        if self.__NewConnection is not None:
            self.__NewConnection = None
        self.Paint()
    
    def SetFocus(self):
        self.picDrawingArea.grab_focus()
   
    @event("pmShowInProjectView","activate")
    def on_mnuShowInProjectView_click(self, menuItem):
        if len(tuple(self.Diagram.GetSelected())) == 1:
            for Element in self.Diagram.GetSelected():
                if isinstance(Element, CElement):
                    self.emit('show-element-in-treeView',Element)
                    
    @event("pmOpenSpecification","activate")
    def on_mnuOpenSpecification_click(self, menuItem):
        if len(tuple(self.Diagram.GetSelected())) == 1:
            for Element in self.Diagram.GetSelected():
                if isinstance(Element, CElement) or isinstance(Element, CConnection):
                    self.__OpenSpecification(Element)
        elif len(tuple(self.Diagram.GetSelected())) == 0:
            self.__OpenSpecification(self.Diagram)
    
    @event("pmShift_SendBack","activate","SendBack")
    @event("pmShift_BringForward","activate","BringForward")
    @event("pmShift_ToBottom","activate","ToBottom")
    @event("pmShift_ToTop","activate", "ToTop")
    def on_pmShift_SendBack_activate(self, menuItem, actionName):
        self.drawingArea.ShiftElements(actionName)
    
    @event("mnuCtxCopy","activate")
    def ActionCopy(self, widget = None):
        self.drawingArea.CopySelectedObjects()
    
    @event("mnuCtxCut", "activate")
    def ActionCut(self, widget = None):
        self.drawingArea.CutSelectedObjects()
    
    @event("mnuCtxPaste","activate")
    def ActionPaste(self, widget = None):
        self.drawingArea.PasteObjects()
    
    @event("mnuCtxDuplicate", "activate")
    def ActionDuplicate(self, widget=None):
        self.drawingArea.DuplicateSelectedObjects()

    @event("mnuCtxShiftDelete","activate")
    def onMnuCtxShiftDelteActivate(self, menuItem):
        self.drawingArea.ShiftDeleteSelectedObjects()
        
    @event("mnuChangeSourceTarget","activate")
    def on_mnuChangeSourceTarget_click(self,widget):
        self.drawingArea.ChangeSourceTarget()
    
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

    def GetSelectionPixbuf(self, zoom, padding, bg):
        (x, y), (sizeX, sizeY) = self.Diagram.GetSelectSquare(True)
        sizeX = (sizeX + padding*2) * zoom
        sizeY = (sizeY + padding*2) * zoom
        canvas = CExportCanvas(self.application.GetProject().GetMetamodel().GetStorage(), 'pixbuf', None, sizeX, sizeY, background = bg)
        canvas.SetScale(zoom)
        canvas.MoveBase(x - padding, y - padding)
        self.Diagram.PaintSelected(canvas)
        return canvas.Finish()
    
    def SelectObject(self, object):
        self.Diagram.AddToSelection(self.Diagram.GetElement(object))                
        y=self.canvas.ToPhysical(self.Diagram.GetSelected().next().position)[1]-self.GetAbsolutePos(self.GetWindowSize())[1]/2
        x=self.canvas.ToPhysical(self.Diagram.GetSelected().next().position)[0]-self.GetAbsolutePos(self.GetWindowSize())[0]/2
        self.SetScrollBarsPosition((x, y))
        self.Paint()

    def __UpdateScrollBarsPosition(self):
        self.SetScrollBarsPosition(self.activeDrawingArea.GetViewPortPos())

    def DeselectAll(self):
        self.activeDiagram.GetSelection().DeselectAll()
    
    @event('application.bus', 'connection-changed')
    @event('application.bus', 'element-changed')
    def ObjectChanged(self, bus, params):
        self.ToPaint()
