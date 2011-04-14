from common import CWidget, event
from lib.Exceptions.UserException import *
from lib.Drawing import CDiagram
import gobject
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject

class CtxtNotes(CWidget):
    name = 'txtNotes'
    widgets = ('txtNotes', )
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
        self.txtNotes.set_sensitive(False)
    
    def Fill(self, Element):
        self.element = Element
        if Element is None:
            self.txtNotes.get_buffer().set_text("")
            self.txtNotes.set_sensitive(False)
            return
        
        object = Element.GetObject()
        if object.GetDomainType().HasAttribute('note'):
            self.txtNotes.get_buffer().set_text(object.GetValue('note'))
            self.txtNotes.set_sensitive(True)
        else:
            self.txtNotes.get_buffer().set_text("")
            self.txtNotes.set_sensitive(False)
    
    @event("txtNotes.buffer", "changed")
    def on_txtNotes_changed(self, buffer):
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        if self.element is not None and self.element.GetObject().GetValue('note') != text:
            self.element.GetObject().SetValue('note', text)
            self.application.GetBus().emit('content-update', self.element, 'note')
                
    @event('application.bus', 'content-update')
    @event('application.bus', 'content-update-from-plugin')
    def on_content_update(self, widget, element, property):
        if self.element is not None and element is self.element:
            self.Fill(self.element)
    