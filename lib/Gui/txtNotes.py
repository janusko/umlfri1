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
        self.element = None
        CWidget.__init__(self, app, wTree)
        self.txtNotes.set_sensitive(False)
    
    def __GetElementObject(self):
        if self.element is None:
            return None
        elif isinstance(self.element, (CElementObject, CConnectionObject, CDiagram)):
            return self.element
        else:
            return self.element.GetObject()
    
    def Fill(self, Element):
        self.element = Element
        if Element is None:
            self.txtNotes.get_buffer().set_text("")
            self.txtNotes.set_sensitive(False)
            return
        
        elementObject = self.__GetElementObject()
        if elementObject.GetDomainType().HasAttribute('note'):
            buffer = self.txtNotes.get_buffer()
            text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
            if text != elementObject.GetValue('note'):
                buffer.set_text(elementObject.GetValue('note'))
            self.txtNotes.set_sensitive(True)
        else:
            self.txtNotes.get_buffer().set_text("")
            self.txtNotes.set_sensitive(False)
    
    @event("txtNotes.buffer", "changed")
    def on_txtNotes_changed(self, buffer):
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        
        elementObject = self.__GetElementObject()
        if self.element is not None and elementObject.GetValue('note') != text:
            elementObject.SetValue('note', text)
            self.application.GetBus().emit('content-update', self.element, 'note')
                
    @event('application.bus', 'content-update')
    @event('application.bus', 'content-update-from-plugin')
    def on_content_update(self, widget, element, property):
        if self.element is not None and element is self.element:
            self.Fill(self.element)
    
    @event('txtNotes', 'focus-in-event')
    def on_focus_in (self, widget, event):
        self.application.GetBus().emit('properties-editing-started')

    @event('txtNotes', 'focus-out-event')
    def on_focus_out (self, widget, event):
        self.application.GetBus().emit('properties-editing-stoped')
