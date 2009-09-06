from common import CWidget, event
from lwProperties import ClwProperties
from txtNotes import CtxtNotes
import gobject

class CnbProperties(CWidget):
    name = 'nbProperties'
    complexWidgets = (ClwProperties, CtxtNotes)

    __gsignals__ = {
        'history-entry':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),        
    }

    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
    
    def Fill(self, element):
        self.lwProperties.Fill(element)
        self.txtNotes.Fill(element)
    
    @event("txtNotes", "history-entry")    
    @event("lwProperties", "history-entry")
    def on_history_entry(self, widget):
        self.emit("history-entry") 