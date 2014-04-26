from common import CWidget, event
from lwProperties import ClwProperties
from txtNotes import CtxtNotes
import gobject

class CnbProperties(CWidget):
    name = 'nbProperties'
    complexWidgets = (ClwProperties, CtxtNotes)
    
    __gsignals__ = {
        'content-update':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)),
        'update_tree':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,)),    
    }
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
    
    def Fill(self, element):
        self.element = element
        self.lwProperties.Fill(element)
        self.txtNotes.Fill(element)
    
    @event("lwProperties", "content-update")
    def on_lwProperties_content_update(self, widget, element, property):    
        self.emit("content-update", element, property)
    
    @event("txtNotes", "content-update")
    def on_txtNotes_content_update(self, widget, element, property):
        self.emit("content-update", element, property)

    @event("lwProperties", "update_tree")
    def on_lwProperties_update_tree(self, widget, elementObj):
        self.emit("update_tree",elementObj)