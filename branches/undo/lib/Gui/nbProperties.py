# -*- coding: utf-8 -*-
from common import CWidget, event
from lwProperties import ClwProperties
from txtNotes import CtxtNotes
import gobject



class CnbProperties(CWidget):
    name = 'nbProperties'
    complexWidgets = (ClwProperties, CtxtNotes)
    
    __gsignals__ = {
        'history-entry':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT, )),
    }
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
    
    def Fill(self, element):
        self.lwProperties.Fill(element)
        self.txtNotes.Fill(element)

    @event("lwProperties", "history-entry")
    def on_history_entry(self, widget, command):
        self.emit("history-entry", command)        
        
    # turned off :), we need a button there or something... maybe a grouping mechanizm ?
    #@event("txtNotes", "history-entry")
    #def on_txtNotes_content_update(self, widget, command):
        #self.emit("history-entry", command)  


    #@event("lwProperties", "content-update")
    #def on_lwProperties_content_update(self, widget, element, property):
        ##self.emit("content-update", element, property)
    
    #@event("txtNotes", "content-update")
    #def on_txtNotes_content_update(self, widget, element, property):
        #self.emit("content-update", element, property)

