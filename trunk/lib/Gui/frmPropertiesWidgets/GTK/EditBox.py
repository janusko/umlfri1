import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractEditBox import CAbstractEditBox

class CEditBox(CAbstractEditBox):
    
    def __init__(self,editable=True):
        self.editbox=gtk.Entry()
        self.editbox.set_property('editable',editable)
        self.editbox.show()
    
    def GetWidget(self):
        return self.editbox
    
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