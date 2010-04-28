# -*- coding: utf-8 -*-
from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

from lib.Project import CProject, CProjectNode

from lib.consts import BUFFER_SIZE, SCALE_MIN, SCALE_MAX, SCALE_INCREASE
from lib.config import config
from lib.Distconfig import IMAGES_PATH

from common import CWidget, event
from lib.Drawing import CDiagram, CElement, CConnection, CConLabelInfo

from lib.Elements import CElementObject
from lib.Connections import CConnectionObject
from lib.Exceptions.UserException import *
from lib.Drawing.Canvas import CGtkCanvas, CSvgCanvas, CCairoCanvas, CExportCanvas
from lib.Drawing import Element
from lib.Drawing.TidyWrap import CTidyWrapper

import thread
import os.path


targets = [('document/uml', 0, gtk.TARGET_SAME_WIDGET)]

class Record(object): pass

class CpicDrawingArea(CWidget):
    name = 'picDrawingArea'
    widgets = ('picDrawingArea', 'picEventBox', 'picVBar', 'picHBar',
                'pMenuShift', 
                'pmShift_SendBack', 'pmShift_BringForward', 'pmShift_ToBottom', 'pmShift_ToTop','pmShowInProjectView',
                'mnuCtxCut', 'mnuCtxCopy', 'mnuCtxPaste', 'mnuCtxDelete',
                'pmOpenSpecification', 'mnuCtxShiftDelete','mnuChangeSourceTarget',
                'pmAlign_Left', 'pmAlign_Right', 'pmAlign_Bottom', 'pmAlign_Top')

    __gsignals__ = {
        'get-selected':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT,
            ()),
        'set-selected':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT, )),
        'selected-item':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT, gobject.TYPE_BOOLEAN, )),
        'run-dialog':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT,
            (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, )), #type, message
        'add-element':(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,gobject.TYPE_PYOBJECT,gobject.TYPE_PYOBJECT,)),
        'delete-element-from-all':(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, )),
        'drop-from-treeview': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
        'show-element-in-treeView': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
        'open-specification': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    }

    def __init__(self, app, wTree):
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
        self.picDrawingArea.realize()
        self.buffer = gtk.gdk.Pixmap(self.picDrawingArea.window, *self.buffer_size[1])
        self.Diagram = CDiagram(None,_("Start page"))
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
        self.cursors = {None: None}
        for name, img in (('grab', 'grab.png'), ('grabbing', 'grabbing.png')):
            self.cursors[name] = gtk.gdk.Cursor(
                gtk.gdk.display_get_default(),
                gtk.gdk.pixbuf_new_from_file(os.path.join(IMAGES_PATH, img)),
                0,
                0
            )
        self.__invalidated = False
        self.lastClick =0,0 

    def __SetCursor(self, cursor = None):
        self.picDrawingArea.window.set_cursor(self.cursors[cursor])
    
    def BestFitScale(self):
        winSizeX, winSizeY = self.GetWindowSize()
        (diaSizeMinX, diaSizeMinY), (diaSizeMaxX, diaSizeMaxY) = self.Diagram.GetSizeSquare(self.canvas)
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

    def SetScale(self, scale):
        if (scale >= SCALE_MIN) and (scale <= SCALE_MAX):
            self.scale = scale
            self.canvas.SetScale(self.scale)
            self.AdjustScrollBars()
            self.Paint()

    def IncScale(self, scale):
        tmp_scale = (SCALE_INCREASE*((self.scale+0.00001)//SCALE_INCREASE))+scale
        if (tmp_scale+0.00001 >= SCALE_MIN) and (tmp_scale-0.00001 <= SCALE_MAX):
            self.scale = tmp_scale
            self.canvas.SetScale(self.scale)
            self.AdjustScrollBars()
            self.Paint()

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
        return self.Diagram

    def SetDiagram(self, diagram):
        #set actual scrolling position before change diagram
        self.Diagram.SetVScrollingPos(int(self.picVBar.get_value()))
        self.Diagram.SetHScrollingPos(int(self.picHBar.get_value()))
        #change diagram
        self.Diagram = diagram
        #load srolling position of new diagram
        self.picHBar.set_value(self.Diagram.GetHScrollingPos())
        self.picVBar.set_value(self.Diagram.GetVScrollingPos())
        self.Paint()

    def GetWindowSize(self):
        tmpx, tmpy =  self.picDrawingArea.window.get_size()
        return (tmpx, tmpy)

    def GetDiagramSize(self):
        tmp = [int(max(i)) for i in zip(self.Diagram.GetSize(self.canvas), self.picDrawingArea.window.get_size())]
        return tuple(tmp)
    
    def GetPos(self):
        return int(self.picHBar.get_value()), int(self.picVBar.get_value())
        
    def SetPos(self, pos = (0, 0)):
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
        try:
            self.paintlock.acquire()
            self.tobePainted = False
            changed = changed or self.paintChanged
            self.paintChanged = False
        finally:
            self.paintlock.release()
        if not self.picDrawingArea.window or not self.canvas:
            if changed:
                self.__invalidated = True # redraw completly on next configure event
            return
        
        posx, posy = int(self.picHBar.get_value()), int(self.picVBar.get_value())
        sizx, sizy = self.GetWindowSize()    
        ((bposx, bposy), (bsizx, bsizy)) = self.buffer_size
        (bposx, bposy) = self.canvas.ToPhysical((bposx, bposy))
        
        
        if posx < bposx or bposx + bsizx < posx + sizx or \
           posy < bposy or bposy + bsizy < posy + sizy:
       
            bposx = posx + (sizx - bsizx)//2
            bposy = posy + (sizy - bsizy)//2
                      
            (bposx, bposy) = self.canvas.ToLogical((bposx, bposy))
            self.buffer_size = ((bposx, bposy), (bsizx, bsizy))
            changed = True
        if changed:
            self.Diagram.SetViewPort(self.buffer_size)
            self.Diagram.Paint(self.canvas)
            
        self.AdjustScrollBars()
        wgt = self.picDrawingArea.window
        gc = wgt.new_gc()
        #def draw_drawable(gc, src, xsrc, ysrc, xdest, ydest, width, height)
        
        wgt.draw_drawable(gc, self.buffer, posx - bposx, posy - bposy, 0, 0, sizx, sizy)
        
        if self.dnd == 'resize':
            self.__DrawResRect((None, None), True, False)  
        elif self.dnd == 'rect':
            self.__DrawDragRect((None, None), True, False)
        elif self.dnd == 'point':
            self.__DrawDragPoint((None, None), True, False)
        elif self.dnd == 'selection':
            self.__DrawDragSel((None, None), True, False)
        if self.__NewConnection is not None:
            self.__DrawNewConnection((None, None), False)

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

    def Export(self, filename, export_type):
        self.Diagram.DeselectAll()
        #what u see export(only currently visible area will be exported): sizeX, sizeY = self.GetWindowSize() 
        sizeX, sizeY = self.Diagram.GetExpSquare(self.canvas)
        canvas = CExportCanvas(self.application.GetProject().GetMetamodel().GetStorage(), export_type, filename, sizeX, sizeY)
        self.Diagram.PaintFull(canvas)
        canvas.Finish()
        self.Paint()    

    def ExportSvg(self, filename):
        # obsolete
        self.Diagram.DeselectAll()
        self.Paint()
        canvas = CSvgCanvas(1000, 1000, self.canvas, self.application.GetProject().GetMetamodel().GetStorage())
        canvas.Clear()
        self.Diagram.Paint(canvas)
        canvas.WriteOut(file(filename, 'w'))
    
    @event("mnuCtxDelete","activate")
    def DeleteElements(self, widget = None):
        for sel in self.Diagram.GetSelected():
            if isinstance(sel, CConnection):
                index = sel.GetSelectedPoint()
                if index is not None and (sel.GetSource() != sel.GetDestination() or len(tuple(sel.GetMiddlePoints())) > 2):
                    sel.RemovePoint(self.canvas, index)
                    self.Diagram.DeselectAll()
                    self.Paint()
                    return
        for sel in self.Diagram.GetSelected():
            self.Diagram.DeleteItem(sel)
        self.Diagram.DeselectAll()
        self.emit('selected-item', list(self.Diagram.GetSelected()),False)
        self.Paint()
    
    def UpdateMenuSensitivity(self, project, diagram, element):
        self.pmShowInProjectView.set_sensitive(element)
        for item in self.pMenuShift.get_children():
            item.set_sensitive(element)
            
        self.mnuCtxPaste.set_sensitive(
            diagram and not self.application.GetClipboard().IsEmpty() and
            not bool(set(i.GetObject() for i in self.Diagram.GetElements()).intersection(set(i.GetObject() for i in self.application.GetClipboard().GetContent())))
        )
        selection = list(self.Diagram.GetSelected())
        self.pmOpenSpecification.set_sensitive(len(selection) == 1)
        self.mnuChangeSourceTarget.set_sensitive(len(selection) == 1)
        if (self.application.GetProject() is not None and 
            self.Diagram is not None and
            self.application.GetProject().GetRoot().GetObject() in (
                [item.GetObject() for item in self.Diagram.GetSelectedElements(True)])):
            self.mnuCtxShiftDelete.set_sensitive(False)
    
    @event("picEventBox", "button-press-event")
    def on_picEventBox_button_press_event(self, widget, event):
        self.picDrawingArea.grab_focus() 
        pos = self.lastClick =self.GetAbsolutePos((event.x, event.y)) # TODO: how to?
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            if len(tuple(self.Diagram.GetSelected())) == 1:
                for Element in self.Diagram.GetSelected():
                    if isinstance(Element, (CElement,CConnection)):
                        self.emit('open-specification',Element)
                        return True
        
        if event.button == 1:
            if gtk.keysyms.space in self.pressedKeys:
                self.__BeginDragMove(event)
                return True
            toolBtnSel = self.emit('get-selected')
            if toolBtnSel is not None:
                self.__AddItem(toolBtnSel, event)
                return True
            
            itemSel = self.Diagram.GetElementAtPosition(self.canvas, pos)
            if itemSel is not None: #something is hit:
                if itemSel in self.Diagram.GetSelected(): # deselecting:
                    if (event.state & gtk.gdk.CONTROL_MASK) or (event.state & gtk.gdk.SHIFT_MASK):
                        self.Diagram.RemoveFromSelection(itemSel)
                        self.Paint()
                        self.emit('selected-item', list(self.Diagram.GetSelected()),False)
                    elif isinstance(itemSel, CConnection): #Connection is selected
                        i = itemSel.GetPointAtPosition(pos)
                        if i is not None:
                            itemSel.SelectPoint(i)
                            self.__BeginDragPoint(event, itemSel, i)
                        else:
                            itemSel.DeselectPoint()
                            i = itemSel.WhatPartOfYouIsAtPosition(self.canvas, pos)
                            self.__BeginDragLine(event, itemSel, i)
                        self.Paint()    
                        self.emit('selected-item', list(self.Diagram.GetSelected()),False)
                    else: #elements are selected
                        self.__BeginDragRect(event)
                elif not (event.state & gtk.gdk.CONTROL_MASK) and not (event.state & gtk.gdk.SHIFT_MASK):
                    self.Diagram.DeselectAll()
                    self.Diagram.AddToSelection(itemSel)
                    if isinstance(itemSel, CConnection):
                        i = itemSel.GetPointAtPosition(pos)
                        if i is not None:
                            itemSel.SelectPoint(i)
                            self.__BeginDragPoint(event, itemSel, i)
                        else:
                            itemSel.DeselectPoint()
                            i = itemSel.WhatPartOfYouIsAtPosition(self.canvas, pos)
                            self.__BeginDragLine(event, itemSel, i)
                    else:
                        selElements = list(self.Diagram.GetSelectedElements())
                        self.selElem = selElements[0]
                        if len(selElements) == 1:
                            self.selSq = self.selElem.GetSquareAtPosition(pos)
                        self.__BeginDragRect(event)
                    self.Paint()
                    self.emit('selected-item', list(self.Diagram.GetSelected()),False)
                else:
                    self.Diagram.AddToSelection(itemSel)
                    self.Paint()
                    self.emit('selected-item', list(self.Diagram.GetSelected()),False)
            else: # nothing under pointer
                if self.Diagram.SelectedCount() > 0:
                    if not (event.state & gtk.gdk.CONTROL_MASK):
                        self.Diagram.DeselectAll()
                        self.Paint()
                        self.emit('selected-item', list(self.Diagram.GetSelected()),False)
                self.__BeginDragSel(event)

        elif event.button == 2:
            self.__BeginDragMove(event)

        elif event.button == 3:
            itemSel = self.Diagram.GetElementAtPosition(self.canvas, pos)
            if itemSel not in frozenset(self.Diagram.GetSelected()):
                self.Diagram.DeselectAll()
            if itemSel is not None:
                self.Diagram.AddToSelection(itemSel)
            self.Paint()
            self.emit('selected-item', list(self.Diagram.GetSelected()),False)
            #if something is selected:
            self.UpdateMenuSensitivity(bool(self.application.GetProject()), bool(self.Diagram), int(len(list(self.Diagram.GetSelected())) > 0))
            self.pMenuShift.popup(None,None,None,event.button,event.time)
            return True

    def __AddItem(self, toolBtnSel, event):
        pos = self.GetAbsolutePos((event.x, event.y))
        if toolBtnSel[0] == 'Element':
            ElementType = self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(toolBtnSel[1])
            ElementObject = CElementObject(ElementType)
            newElement = CElement(self.Diagram, ElementObject)
            newElement.SetPosition(pos)
            self.AdjustScrollBars()
            self.emit('set-selected', None)
            #here, I get prent element of selected elements (if element is on (over) another element)
            minzorder = 9999999
            parentElement = None
            for el in self.Diagram.GetSelectedElements(True):
                pos1, pos2 = el.GetSquare(self.canvas)
                zorder = self.Diagram.GetElementZOrder(el)
                if newElement.AreYouInRange(self.canvas, pos1, pos2, True):
                    for el2 in self.Diagram.GetElementsInRange(self.canvas, pos1, pos2, True):
                        if self.Diagram.GetElementZOrder(el2) < minzorder:        #get element with minimal zorder
                            minzorder = self.Diagram.GetElementZOrder(el2)
                            parentElement = el2.GetObject()
                    
            self.Diagram.DeselectAll()
            self.emit('add-element', ElementObject, self.Diagram, parentElement)
            self.Diagram.AddToSelection(newElement)
            self.emit('selected-item', list(self.Diagram.GetSelected()),True)
            self.Paint()

        elif toolBtnSel[0] == 'Connection':
            itemSel = self.Diagram.GetElementAtPosition(self.canvas, pos)

            if itemSel is None:
                if self.__NewConnection is not None:
                    pass
            elif isinstance(itemSel, CConnection):
                return
            elif self.__NewConnection is None:
                ConnectionType = self.application.GetProject().GetMetamodel().GetConnectionFactory().GetConnection(toolBtnSel[1])
                center = itemSel.GetCenter(self.canvas)
                relcenter = self.GetRelativePos(center)
                self.__NewConnection = (ConnectionType, [center], itemSel)
                self.__DrawNewConnection(relcenter, False)
            else:
                pass

    @event("picEventBox", "button-release-event")
    def on_button_release_event(self, widget, event):
        try:
            if self.dnd == 'resize':
                delta = self.__GetDelta((event.x, event.y), True)
                self.selElem.Resize(self.canvas, delta, self.selSq)
                self.selElem = None
                self.selSq = None
                self.dnd = None 
            elif self.dnd == 'rect':
                delta = self.__GetDelta((event.x, event.y))
                self.Diagram.MoveSelection(delta, self.canvas)
                self.dnd = None
            elif self.dnd == 'point':
                point = self.GetAbsolutePos((event.x, event.y))
                connection, index = self.DragPoint
                connection.MovePoint(self.canvas, point, index)
                self.dnd = None
            elif self.dnd == 'line':
                point = self.GetAbsolutePos((event.x, event.y))
                connection, index = self.DragPoint
                connection.InsertPoint(self.canvas, point, index)
                self.dnd = None
            elif self.dnd == 'move':
                if gtk.keysyms.space in self.pressedKeys:
                    self.__SetCursor('grab')
                else:
                    self.__SetCursor(None)
                self.dnd = None
            elif self.dnd == 'selection':
                x1, y1 = self.DragSel
                x2, y2 = self.GetAbsolutePos((event.x, event.y))
                if x2 < x1:
                    x2, x1 = x1, x2
                if y2 < y1:
                    y2, y1 = y1, y2
                self.Diagram.AddRangeToSelection(self.canvas, (x1, y1), (x2, y2))
                self.dnd = None
                self.emit('selected-item', list(self.Diagram.GetSelected()),False)
            elif self.__NewConnection is not None:
                pos = self.GetAbsolutePos((event.x, event.y))
                itemSel = self.Diagram.GetElementAtPosition(self.canvas, pos)
                if itemSel is None or isinstance(itemSel, CConnection):
                    self.__NewConnection[1].append(pos)
                    self.__DrawNewConnection((None, None))
                elif itemSel is not self.__NewConnection[2] or len(self.__NewConnection[1]) > 2:
                    (type, points, source), destination = self.__NewConnection, itemSel
                    obj = CConnectionObject(type, source.GetObject(), destination.GetObject())
                    x = CConnection(self.Diagram, obj, source, destination, points[1:])
                    self.emit('set-selected', None)
                    self.Diagram.AddToSelection(x)
                    self.emit('selected-item', list(self.Diagram.GetSelected()),True)
                    self.__NewConnection = None
                else:
                    pass
            else:
                return
            self.AdjustScrollBars()
            self.Paint()
        except ConnectionRestrictionError:
            self.ResetAction()
            self.emit('set-selected', None)
            self.emit('run-dialog', 'warning', _('Invalid connection'))
    
    @event("picEventBox", "key-press-event")
    def on_key_press_event(self, widget, event):
        if (event.keyval in self.pressedKeys and
            event.keyval not in (gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Up, gtk.keysyms.Down)):
            return True
        self.pressedKeys.add(event.keyval)
        if event.keyval==gtk.keysyms.a and event.state == gtk.gdk.CONTROL_MASK:
            self.Diagram.SelectAll()
            self.emit('selected-item', list(self.Diagram.GetSelected()),False)
            self.Paint()
        elif event.keyval == gtk.keysyms.Delete:
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
                if self.dnd is None: #Zacinam posuvat
                    self.keydragPosition = list(selected[0].GetCenter(self.canvas))
                    e = Record()
                    e.x, e.y = self.keydragPosition
                    self.__BeginDragRect(e)
                if self.dnd == 'rect':
                    if self.keydragPosition is None:
                        self.keydragPosition = list(selected[0].GetCenter(self.canvas))
                    if gtk.keysyms.Right in self.pressedKeys:
                        self.keydragPosition[0] += 10
                    if gtk.keysyms.Left in self.pressedKeys:
                        self.keydragPosition[0] -= 10
                    if gtk.keysyms.Up in self.pressedKeys:
                        self.keydragPosition[1] -= 10
                    if gtk.keysyms.Down in self.pressedKeys:
                        self.keydragPosition[1] += 10
                    self.__DrawDragRect(self.keydragPosition)
        return True
    
    @event("picEventBox", "key-release-event")
    def on_key_release_event(self, widget, event):
        if gtk.keysyms.space in self.pressedKeys:
            if self.dnd != 'move':
                self.__SetCursor(None)
        
        self.pressedKeys.discard(event.keyval)
        
        if (event.keyval in (gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Up, gtk.keysyms.Down) 
            and set() == self.pressedKeys.intersection(set([gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Up, gtk.keysyms.Down]))
            and self.dnd == 'rect'):
            
            delta = self.__GetDelta(self.keydragPosition)
            self.keydragPosition = None
            self.Diagram.MoveSelection(delta, self.canvas)
            self.dnd = None
            self.Paint()

    @event("picEventBox", "motion-notify-event")
    def on_motion_notify_event(self, widget, event):
        if self.dnd == 'resize':
            self.__DrawResRect((event.x, event.y), True, True)    
        elif self.dnd == 'rect' and self.keydragPosition is None:
            self.__DrawDragRect((event.x, event.y))
        elif self.dnd == 'point':
            self.__DrawDragPoint((event.x, event.y))
        elif self.dnd == 'line':
            self.__DrawDragLine(event.x, event.y)
        elif self.dnd == 'move':
            self.__DrawDragMove((event.x, event.y))
        elif self.dnd == 'selection':
            self.__DrawDragSel((event.x, event.y))
        elif self.__NewConnection is not None:
            self.__DrawNewConnection((event.x, event.y))

    
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
        self.Paint(False)

    @event("picHBar", "value-changed")
    def on_picHBar_value_changed(self, widget):
        self.Paint(False)

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
        else:
            self.selSq = None
        
        self.DragRect = (self.Diagram.GetSelectSquare(self.canvas))
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
                
    def __DrawResRect(self, pos, erase = True, draw = True):
        if erase:
            x1 = self.DragRect[0][0]
            y1 = self.DragRect[0][1]            
            x2,y2 = self.canvas.ToPhysical(self.DragRect[1])
            self.picDrawingArea.window.draw_rectangle(self.DragGC, False, x1, y1, x2, y2)
        if draw:
            delta = self.__GetDelta(pos, True)
            rect = self.selElem.GetResizedRect(self.canvas, delta, self.selSq)
            rect = self.GetRelativePos(rect[0]), rect[1]
            x2,y2 = self.canvas.ToPhysical(rect[1])
            self.picDrawingArea.window.draw_rectangle(self.DragGC, False, rect[0][0], rect[0][1], x2, y2)
            self.DragRect = rect

    def __DrawDragPoint(self, (x, y), erase = True, draw = True):
        if x is None:
            x, y = self.__oldPoints2
        connection, index = self.DragPoint
        prev, next = connection.GetNeighbours(index, self.canvas)
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
        all = tuple(connection.GetPoints(self.canvas))
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
        self.SetPos((posx - x1 + x2, posy - y1 + y2))
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
                    self.emit('open-specification',Element)
        
    # Z-Order menu:  
    def Shift_activate(self, actionName):
        if (actionName == 'SendBack'):
            self.Diagram.ShiftElementsBack(self.canvas)
        elif (actionName == 'BringForward'):
            self.Diagram.ShiftElementsForward(self.canvas)
        elif (actionName == 'ToBottom'):
            self.Diagram.ShiftElementsToBottom()
        elif (actionName == 'ToTop'):
            self.Diagram.ShiftElementsToTop()
        self.Paint()
    
    @event("pmShift_SendBack","activate")
    def on_pmShift_SendBack_activate(self, menuItem):
        self.Shift_activate('SendBack')
        
    @event("pmShift_BringForward","activate")
    def on_pmShift_BringForward_activate(self, menuItem):
        self.Shift_activate('BringForward')       
      
    @event("pmShift_ToBottom","activate")
    def on_pmShift_ToBottom_activate(self, menuItem):
        self.Shift_activate('ToBottom')                
      
    @event("pmShift_ToTop","activate")
    def on_pmShift_ToTop_activate(self, menuItem):
        self.Shift_activate('ToTop')
    
    @event("mnuCtxCopy","activate")
    def ActionCopy(self, widget = None):
        self.Diagram.CopySelection(self.application.GetClipboard())
    
    @event("mnuCtxCut", "activate")
    def ActionCut(self, widget = None):
        self.Diagram.CutSelection(self.application.GetClipboard())
        self.Paint()
        self.emit('selected-item', list(self.Diagram.GetSelected()),False)
    
    @event("mnuCtxPaste","activate")
    def ActionPaste(self, widget = None):
        self.Diagram.PasteSelection(self.application.GetClipboard())
        self.Paint()
        self.emit('selected-item', list(self.Diagram.GetSelected()),False)
        
    @event("mnuCtxShiftDelete","activate")
    def onMnuCtxShiftDelteActivate(self, menuItem):
        for sel in self.Diagram.GetSelected():
            if isinstance(sel, Element.CElement):
                self.emit('delete-element-from-all',sel.GetObject())
            elif isinstance(sel, CConLabelInfo):
                self.Diagram.ShiftDeleteConLabel(sel)
            else:
                self.Diagram.ShiftDeleteConnection(sel)
        self.Paint()
        
    @event("mnuChangeSourceTarget","activate")
    def on_mnuChangeSourceTarget_click(self,widget):
        self.ChangeSourceTarget()
        self.Paint()
        
        
    def ChangeSourceTarget(self):
        
        for sel in self.Diagram.GetSelected():
            if isinstance(sel, CConnection):
                sel.GetObject().ChangeConnection()
            project = self.application.GetProject()
            diagrams = project.GetDiagrams()
            for d in diagrams:
                for c in d.GetConnections():
                    if c.GetObject() == sel.GetObject():
                        c.ChangeConnection(self.canvas)                        
                        self.Paint()
                
    def HasFocus(self):
        return self.picDrawingArea.is_focus()

    def GetSelectionPixbuf(self, zoom, padding, bg):
        (x, y), (sizeX, sizeY) = self.Diagram.GetSelectSquare(self.canvas, True)
        sizeX = (sizeX + padding*2) * zoom
        sizeY = (sizeY + padding*2) * zoom
        canvas = CExportCanvas(self.application.GetProject().GetMetamodel().GetStorage(), 'pixbuf', None, sizeX, sizeY, background = bg)
        canvas.SetScale(zoom)
        canvas.MoveBase(x - padding, y - padding)
        self.Diagram.PaintSelected(canvas)
        return canvas.Finish()

    ### Align & tidy methods
    # Takes all selected Elements (ONLY Elements, no Labels or Connections!)
    #left
    @event("pmAlign_Left","activate")
    def alignLeft(self, widget = None):
        # get the LEFT edge of clicked Element
        clickedElem =self.Diagram.GetElementAtPosition(self.canvas, self.lastClick)
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignLeft( clickedElem)
        a.applyState()
        # redraw canvas!
        self.Paint()
    
    def alignMostLeft(self, widget = None):
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignMostLeft()
        a.applyState()
        # redraw canvas!
        self.Paint()
    
    #right
    @event("pmAlign_Right","activate")
    def alignRight(self, widget = None):
        # get the RIGHT edge of clicked Element
        clickedElem =self.Diagram.GetElementAtPosition(self.canvas, self.lastClick)
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignRight( clickedElem)
        a.applyState()
        # redraw canvas!
        self.Paint()
    
    def alignMostRight(self, widget = None):
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignMostRight()
        a.applyState()
        # redraw canvas!
        self.Paint()
    
    #top
    @event("pmAlign_Top","activate")
    def alignTop(self, widget = None):
        # get the TOP edge of clicked Element
        clickedElem =self.Diagram.GetElementAtPosition(self.canvas, self.lastClick)
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignTop( clickedElem)
        a.applyState()
        # redraw canvas!
        self.Paint()
    
    def alignMostTop(self, widget = None):
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignMostTop()
        a.applyState()
        # redraw canvas!
        self.Paint()
    
    #bottom
    @event("pmAlign_Bottom","activate")
    def alignBottom(self, widget = None):
        # get the BOTTOM edge of clicked Element
        clickedElem =self.Diagram.GetElementAtPosition(self.canvas, self.lastClick)
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignBottom( clickedElem)
        a.applyState()
        # redraw canvas!
        self.Paint()
    
    def alignMostBottom(self, widget = None):
        # use the algorithm for Alignment
        a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram )
        a.alignMostBottom()
        a.applyState()
        # redraw canvas!
        self.Paint()

    #TIDY
    #@event("pmTidy","activate")
    def Tidy(self, widget = None):
        # use the algorithm for Tidy
        #a =CTidyWrapper( self.Diagram.GetSelectedElements(), self.Diagram,  )
        #a.Tidy( modus)
        # TODO Calling of the tidy
        #a.applyState()
        # redraw canvas!
        self.Paint()
