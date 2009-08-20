from common import CWidget, event
from lwProperties import ClwProperties
from txtNotes import CtxtNotes
import gobject

class CnbProperties(CWidget):
    name = 'nbProperties'
    complexWidgets = (ClwProperties, CtxtNotes)
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
    
    def Fill(self, element):
        self.lwProperties.Fill(element)
        self.txtNotes.Fill(element)
    
