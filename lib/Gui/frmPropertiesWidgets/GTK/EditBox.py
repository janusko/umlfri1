import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractEditBox import CAbstractEditBox

class CEditBox(CAbstractEditBox):
    
    def __init__(self,editable=True,style='text'):
        self.editbox=gtk.Entry()
        self.editbox.set_property('editable',editable)
        if style=='int' or style=='float':
            self.editbox.connect('key-press-event',self.__EditBoxInputHandler,style)
        self.lastkey=-1
        self.editbox.show()
    
    def GetWidget(self):
        return self.editbox
    
    def SetBackgroundColor(self,color):
        self.editbox.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))
    
    def SetText(self,text):
        self.editbox.set_text(text)
    
    def GetText(self):
        return self.editbox.get_text()
    
    def SetHandler(self,event,func,data=None):
        if event=='changed':
            self.editbox.connect('changed',self.__EditBoxEventHandler,func,data)
    
    def __EditBoxEventHandler(self,editbox,func,data):
        if data!=None:
            func(*data)
        else:
            func()
    
    def __EditBoxInputHandler(self,entry,event,style):
        keys=(45,48,49,50,51,52,53,54,55,56,57,65360,65361,65362,65363,65364,65367,65289,65288,65535)
        if style=='float':
            keys+=tuple([46])
        if not event.keyval in keys:
            if self.lastkey!=65507 or not event.keyval in(99,118,120):
                self.lastkey = event.keyval
                return True
            else:
                return False
            return True