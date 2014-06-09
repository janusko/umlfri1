from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

from lib.Drawing.PixmapImageLoader import PixmapFromPath

from common import CWidget, event
from lib.Commands.Project import CCreateElementObjectCommand, CCreateDiagramCommand

class CmnuItems(CWidget):
    name = 'mnuItems'
    widgets = ('mItemAddDiagram_menu','mItemAddElement_menu',)
    
    __gsignals__ = {
        'create-diagram':   (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
        'add-element':   (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    }

    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
        
        self.__selectedNode = None

    def Redraw(self):
        """
        This function load Project Add menu from enabled diagrams and options of elements
        
        """
        for item in self.mItemAddDiagram_menu.get_children():
            self.mItemAddDiagram_menu.remove(item)
        
        for item in self.mItemAddElement_menu.get_children():
            self.mItemAddElement_menu.remove(item)

        for item in self.application.GetProject().GetMetamodel().GetElementFactory().IterTypes():
            if item.GetOptions().get('DirectAdd', False):
                newItem = gtk.ImageMenuItem(item.GetId())
                self.mItemAddElement_menu.append(newItem)
                newItem.connect("activate", self.on_mnuAddElement_activate, item.GetId())
                img = gtk.Image()
                img.set_from_pixbuf(PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(item.GetId()).GetIcon()))
                newItem.set_image(img)
                img.show()
                newItem.show()
        
        for diagram in self.application.GetProject().GetMetamodel().GetDiagrams():
            newItem = gtk.ImageMenuItem(diagram)
            newItem.connect("activate", self.on_mnuDiagrams_activate, diagram)
            img = gtk.Image()
            img.set_from_pixbuf(PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), self.application.GetProject().GetMetamodel().GetDiagramFactory().GetDiagram(diagram).GetIcon()))
            img.show()
            newItem.set_image(img)
            self.mItemAddDiagram_menu.append(newItem)
            newItem.show()
    
    @event("application.bus", "project-selection-changed")
    def on_project_selection_changed(self, bus, selectedNode):
        self.__selectedNode = selectedNode
        
    def on_mnuDiagrams_activate(self, widget, diagramId):
        if self.__selectedNode is None:
            return
        type = self.application.GetProject().GetMetamodel().GetDiagramFactory().GetDiagram(diagramId)
        cmd = CCreateDiagramCommand(type, self.__selectedNode)
        self.application.GetCommands().Execute(cmd)
    
    def on_mnuAddElement_activate(self, widget, element):
        if self.__selectedNode is None:
            return
        type = self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(element)
        cmd = CCreateElementObjectCommand(type, self.__selectedNode)
        self.application.GetCommands().Execute(cmd)
        
