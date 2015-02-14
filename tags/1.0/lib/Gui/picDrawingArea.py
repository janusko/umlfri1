from lib.Commands.Diagrams.DuplicateElements import CDuplicateElementsCommand
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
        'selected-item':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT, gobject.TYPE_BOOLEAN, )),
        'run-dialog':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT,
            (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, )), #type, message
        'delete-element-from-all':(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
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
    
    def __OpenSpecification(self, obj):
        frmProps = self.application.GetWindow('frmProperties')
        frmProps.SetParent(self.application.GetWindow('frmMain'))
        frmProps.ShowPropertiesWindow(obj, self.application)

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
            self.disablePaint = True
            self.CenterZoom(scale)
            self.canvas.SetScale(self.scale)
            self.AdjustScrollBars()
            self.disablePaint = False
            self.Paint()

    def ShiftScrollbars(self, direction):
        posx,posy = self.GetPos()
        if(self.getPlusMove > 0):
            move = int(self.getPlusMove / 2)
        else:
            move = 5
        if(direction == "right"):
            self.SetPos((posx + move, posy))
        if(direction == "left"):
            self.SetPos((posx - move, posy))
        if(direction == "up"):
            self.SetPos((posx, posy+move))
        if(direction == "down"):
            self.SetPos((posx, posy-move))
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

    def CenterZoom(self, scale):
        positionH = 0.0
        positionW = 0.0
        shift = 180
        elements = tuple(self.Diagram.GetSelectedElements())
        if (len(elements)>0):
            avgH = 0
            avgW = 0
            for e in elements:
                avgW += e.GetCenter(self.canvas)[0]
                avgH += e.GetCenter(self.canvas)[1]
            avgH = avgH/len(elements)
            avgW = avgW/len(elements)
            positionH = avgH/5.0
            positionW = avgW/5.0

            if(scale > 0): #INZOOM
                pos1 = self.GetPos()[1]
                pos2 = self.GetPos()[0]
                if(avgH>shift):
                    pos1 += positionH
                else:
                    pos1 = 0
                if(avgW>shift):
                    pos2 += positionW
                else:
                    pos2 = 0
                self.SetPos((pos2,pos1))
            else: #OUTZOOM
                pos1 = self.GetPos()[1]
                pos2 = self.GetPos()[0]
                if(avgH>shift):
                    pos1 -= positionH
                else:
                    pos1 = 0
                if(avgW>shift):
                    pos2 -= positionW
                else:
                    pos2 = 0
                self.SetPos((pos2,pos1))
            
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

        if self.disablePaint:
            return
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

        if(self.adjScrollbars != ""):
            self.ShiftScrollbars(self.adjScrollbars)
            self.adjScrollbars = ""

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

    def Export(self, filename, export_type, zoom, padding, background=None):
        self.Diagram.DeselectAll()
        
        (x1, y1), (x2, y2) = self.Diagram.GetSizeSquare(self.canvas)
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
    
    def UpdateMenuSensitivity(self, project, diagram, element, topElement, connection):
        self.pmShowInProjectView.set_sensitive(element)
        for item in self.pMenuShift.get_children():
            item.set_sensitive(element)
            
        self.mnuCtxPaste.set_sensitive(
            diagram and not self.application.GetClipboard().IsEmpty()
            # enable pasting duplicate elements, duplicity is handled in diagram.PasteSelecton
            # and not bool(set(i.GetObject() for i in self.Diagram.GetElements()).intersection(set(i.GetObject() for i in self.application.GetClipboard().GetContent())))
        )
        
        selection = list(self.Diagram.GetSelected())
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
            self.ToPaint()
        else:
            self.Paint()
    
    @event('application.bus', 'properties-editing-started')
    def on_properties_editing_started (self, widget):
        self.pMenuShift.set_sensitive (False)

    @event('application.bus', 'properties-editing-stoped')
    def on_properties_editing_ended (self, widget):
        self.pMenuShift.set_sensitive (True)

    @event("picEventBox", "button-press-event")
    def on_picEventBox_button_press_event(self, widget, event):
        self.picDrawingArea.grab_focus() 
        pos = self.GetAbsolutePos((event.x, event.y))
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            if len(tuple(self.Diagram.GetSelected())) == 1:
                for Element in self.Diagram.GetSelected():
                    if isinstance(Element, (CElement,CConnection)):
                        self.__OpenSpecification(Element)
                        return True
            elif len(tuple(self.Diagram.GetSelected())) == 0:
                self.__OpenSpecification(self.Diagram)
        
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
                        #self.Paint()
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
                        #self.Paint()
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
                    #self.Paint()
                    self.emit('selected-item', list(self.Diagram.GetSelected()),False)
                else:
                    self.Diagram.AddToSelection(itemSel)
                    #self.Paint()
                    self.emit('selected-item', list(self.Diagram.GetSelected()),False)
            else: # nothing under pointer
                if self.Diagram.SelectedCount() > 0:
                    if not (event.state & gtk.gdk.CONTROL_MASK):
                        self.Diagram.DeselectAll()
                        #self.Paint()
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
            #self.UpdateMenuSensitivity(bool(self.application.GetProject()), bool(self.Diagram), int(len(list(self.Diagram.GetSelected())) > 0))
            self.itemSel = itemSel
            self.pMenuShift.popup(None,None,None,event.button,event.time)
            return True

    def __AddItem(self, toolBtnSel, event):
        pos = self.GetAbsolutePos((event.x, event.y))
        if toolBtnSel[0] == 'Element':
            ElementType = self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(toolBtnSel[1])
            ElementObject = CElementObject(ElementType)
            newElement = CElement(self.Diagram, ElementObject)
            newElement.SetPosition(pos)
            self.Diagram.MoveElement(newElement, pos, self.canvas)
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
            self.application.GetBus().emit('add-element', ElementObject, self.Diagram, parentElement)
            self.Diagram.AddToSelection(newElement)
            self.emit('selected-item', list(self.Diagram.GetSelected()),True)
            self.Paint()

        elif toolBtnSel[0] == 'Connection':
            itemSel = self.Diagram.GetElementAtPosition(self.canvas, pos)

            if itemSel is None:
                if self.__NewConnection is not None:
                    pass
            elif isinstance(itemSel, (CConnection, CConLabelInfo)):
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
                self.Diagram.MoveConnectionPoint(connection, point, index, self.canvas)
                self.dnd = None
            elif self.dnd == 'line':
                point = self.GetAbsolutePos((event.x, event.y))
                connection, index = self.DragPoint
                if connection.InsertPoint(self.canvas, point, index):
                    self.Diagram.MoveConnectionPoint(connection, point, index+1, self.canvas)
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
                if itemSel is None or isinstance(itemSel, (CConnection, CConLabelInfo)):
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
                    self.keydragPosition = list(selected[0].GetCenter(self.canvas))
                    e = Record()
                    e.x, e.y = self.keydragPosition
                    self.__BeginDragRect(e)
                if self.dnd == 'rect':
                    if self.keydragPosition is None:
                        self.keydragPosition = list(selected[0].GetCenter(self.canvas))
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
            if(self.setResize == False):
                self.selSq = None
                self.setResize = True
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
                    self.__OpenSpecification(Element)
        elif len(tuple(self.Diagram.GetSelected())) == 0:
            self.__OpenSpecification(self.Diagram)
        
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
    
    @event("mnuCtxDuplicate", "activate")
    def ActionDuplicate(self, widget=None):
#        duplicates = self.Diagram.DuplicateSelectedElements()
#        self.Diagram.DeselectAll()
#        for element in duplicates:
#            self.emit('add-element', element.GetObject(), self.Diagram, None)
#            self.Diagram.AddToSelection(element)
#        self.emit('selected-item', list(self.Diagram.GetSelected()),True)
        cmd  = CDuplicateElementsCommand(tuple(self.Diagram.GetSelectedElements()), self.Diagram)
        self.application.GetCommands().Execute(cmd)
        self.Paint()

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
    
    @event("mnuAlignLeftMost","activate", True, True, False)
    @event("mnuAlignLeftCurrent","activate", True, True, True)
    @event("mnuAlignRightMost","activate", True, False, False)
    @event("mnuAlignRightCurrent","activate", True, False, True)
    @event("mnuAlignUpwardsMost","activate", False, True, False)
    @event("mnuAlignUpwardsCurrent","activate", False, True, True)
    @event("mnuAlignDownwardsMost","activate", False, False, False)
    @event("mnuAlignDownwardsCurrent","activate", False, False, True)
    def on_mnuAlign_activate(self, menuItem, horiz, lower, defaultE):
        self.Diagram.AlignElementsXY(horiz, lower, self.canvas, self.itemSel if defaultE else None)
        self.Paint()
    
    @event("mnuAlignCenterHor","activate", True, True)
    @event("mnuAlignCenterVer","activate", False, True)
    def on_mnuAlignCenter(self, widget, p1, p2):
        self.Diagram.AlignElementCentersXY(p1, self.canvas, self.itemSel if p2 else None)
        self.Paint()
    
    @event("mnuResizeHight","activate")
    def on_mnuResizeHight(self, menuItem):
        self.Diagram.ResizeElementsEvenly(False,self.canvas,self.itemSel)
        self.Paint()
        
    @event("mnuResizeWidth","activate")
    def on_mnuResizeWidth(self, menuItem):
        self.Diagram.ResizeElementsEvenly(True,self.canvas,self.itemSel)
        self.Paint()
    
    @event("mnuResizeHightAndWidth","activate")
    def on_mnuResizeWidthAndHight(self, menuItem):
        self.Diagram.ResizeElementsEvenly(True,self.canvas,self.itemSel)
        self.Diagram.ResizeElementsEvenly(False,self.canvas,self.itemSel)
        self.Paint()
    
    @event("mnuResizeByMaximalElement","activate")
    def on_mnuResizeByMaximalElement(self, menuItem):
        self.Diagram.ResizeByMaximalElement(self.canvas)        
        self.Paint()
        
    @event("mnuResizeByMinimalElement","activate")
    def on_mnuResizeByMinimalElement(self, menuItem):
        self.Diagram.ResizeByMinimalElement(self.canvas)        
        self.Paint()
    
    @event("mnuSpaceEvenlyHorizontally","activate", True)
    @event("mnuSpaceEvenlyVertically","activate", False)
    def on_mnuMakeSpacing(self, widget, p1):
        self.Diagram.SpaceElementsEvenlyXY(p1, self.canvas)
        self.Paint()
    
    @event('mnuSnapSelectGrid', 'activate')
    def on_mnuSnapSelected(self, widget):
        self.Diagram.SnapElementsOnGrid(self.canvas)
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
                        c.ChangeConnection()
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
    
    def SelectObject(self, object):
        self.Diagram.AddToSelection(self.Diagram.GetElement(object))                
        y=self.canvas.ToPhysical(self.Diagram.GetSelected().next().position)[1]-self.GetAbsolutePos(self.GetWindowSize())[1]/2
        x=self.canvas.ToPhysical(self.Diagram.GetSelected().next().position)[0]-self.GetAbsolutePos(self.GetWindowSize())[0]/2
        self.SetPos((x, y))
        self.Paint()
    
    @event('application.bus', 'connection-changed')
    @event('application.bus', 'element-changed')
    def ObjectChanged(self, bus, params):
        self.ToPaint()