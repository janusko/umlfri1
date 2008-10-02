from common import CWidget, event
from lib.Exceptions.UserException import *
from lib.Drawing import CDiagram
import gobject

class CtxtNotes(CWidget):
    name = 'txtNotes'
    widgets = ('txtNotes', )
    
    __gsignals__ = {
        'content-update':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)),
    }
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
        self.txtNotes.set_sensitive(False)
    
    def Fill(self, Element):
        self.element = Element
        if Element is None:
            self.txtNotes.get_buffer().set_text("")
            self.txtNotes.set_sensitive(False)
            return
        
        if isinstance(self.element, CDiagram):
            return
        
        object = Element.GetObject()
        DObject = object.GetDomainObject()
        DType = DObject.GetType()
        if DType.HasAttribute('note'):
            self.txtNotes.get_buffer().set_text(DObject.GetValue('note'))
            self.txtNotes.set_sensitive(True)
    
    @event("txtNotes.buffer", "changed")
    def on_txtNotes_changed(self, buffer):
        if self.element is not None:
            if isinstance(self.element, CDiagram):
                pass    #maybe, In the future, We can add notes to diagram
            else:
                self.element.GetObject().GetDomainObject().SetValue('note', buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter()))
                self.emit('content_update', self.element)
