import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractTextArea import CAbstractTextArea

class CTextArea(CAbstractTextArea):
    
    def __init__(self):
        self.textarea=gtk.TextView()
        self.textarea.show()
        sw=gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        sw.add(self.textarea)
        sw.show()
        self.frm=gtk.Frame()
        self.frm.show()
        self.frm.add(sw)
    
    def GetWidget(self):
        return self.frm
    
    def GetText(self):
        buffer=self.textarea.get_buffer()
        return buffer.get_text(buffer.get_iter_at_offset(0),buffer.get_iter_at_offset(buffer.get_char_count()),True)
    
    def SetText(self,text):
        self.textarea.get_buffer().set_text(text)
    
    def SetHandler(self,event,func,data=None):
        if event=='changed':
            self.textarea.get_buffer().connect('changed',self.__ButtonEventHandler,func,data)
    
    def __ButtonEventHandler(self,button,func,data):
        if data!=None:
            func(*data)
        else:
            func()