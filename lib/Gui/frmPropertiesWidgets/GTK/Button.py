import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractButton import CAbstractButton

class CButton(CAbstractButton):
    
    def __init__(self,title=''):
        self.button=gtk.Button(title)
        self.button.set_size_request(82,26)
        self.button.show()
    
    def GetWidget(self):
        return self.button
    
    def SetSize(self,x,y):
        self.button.set_size_request(x,y)
    
    def GrabFocus(self):
        self.button.grab_focus()
    
    def SetSensitive(self,value):
        self.button.set_sensitive(value)
    
    def SetHandler(self,event,func,data):
        if event=='clicked':
            self.button.connect('clicked',self.__ButtonEventHandler,func,data)
    
    def __ButtonEventHandler(self,button,func,data):
        if data!=None:
            func(*data)
        else:
            func()
    