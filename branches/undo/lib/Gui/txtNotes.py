from common import CWidget, event
from lib.Exceptions.UserException import *
from lib.Drawing import CDiagram
import gobject
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Commands.PropertiesCommands import CElementChangeCmd


class CtxtNotes(CWidget):
    name = 'txtNotes'
    widgets = ('txtNotes', )
    
    __gsignals__ = {
        'history-entry':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),       
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
        if isinstance(object, (CElementObject, CConnectionObject)):
            if object.GetDomainType().HasAttribute('note'):
                self.txtNotes.get_buffer().set_text(object.GetValue('note'))
                self.txtNotes.set_sensitive(True)
        elif isinstance(object, CConnectionObject):
            type = Element.GetObject().GetType()
            cnt = 0
            for k in type.GetAttributes():
                v = object.GetAttribute(k)
                atrtype = type.GetAttribute(k)
                if atrtype[0] == 'note':
                    if cnt > 0:
                        self.element = None
                        raise ProjectError("TooMuchNotes")
                    self.txtNotes.get_buffer().set_text(v)
                    self.txtNotes.set_sensitive(True)
                    self.attr = k
                    cnt += 1
    @event("txtNotes", "focus-out-event")
    def kuk(self, widget, event):
        if self.element is not None:
            if isinstance(self.element, CDiagram):
                pass    #maybe, In the future, We can add notes to diagram
            elif isinstance(self.element.GetObject(), (CElementObject, CConnectionObject)):
                elementChange = CElementChangeCmd(self.element, 'note', self.txtNotes.get_buffer().get_text(self.txtNotes.get_buffer().get_start_iter(), self.txtNotes.get_buffer().get_end_iter())) 
                self.application.history.Add(elementChange)
                self.emit('history-entry')
            elif isinstance(self.element.GetObject(), CConnectionObject):
                elementChange = CElementChangeCmd(self.element, self.attr, self.txtNotes.get_buffer().get_text(self.txtNotes.get_buffer().get_start_iter(), self.txtNotes.get_buffer().get_end_iter())) 
                self.application.history.Add(elementChange)
                self.emit('history-entry')


    @event("txtNotes.buffer", "changed")
    def on_txtNotes_changed(self, buffer):
        pass
