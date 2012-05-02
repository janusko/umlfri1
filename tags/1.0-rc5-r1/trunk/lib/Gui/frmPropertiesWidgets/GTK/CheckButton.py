import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractCheckButton import CAbstractCheckButton

class CCheckButton(CAbstractCheckButton):
    
    def __init__(self,title=''):
        self.button=gtk.CheckButton(title)
        self.button.show()
    
    def GetWidget(self):
        return self.button
    
    def IsChecked(self):
        return self.button.get_active()
    
    def SetHandler(self,event,func,data):
        if event=='toggled':
            self.button.connect('toggled',self.__ButtonEventHandler,func,data)
    
    def __ButtonEventHandler(self,button,func,data):
        func(*data)
    