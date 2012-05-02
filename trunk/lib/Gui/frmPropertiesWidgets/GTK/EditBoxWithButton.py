import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.GTK.Button import CButton
from lib.Gui.frmPropertiesWidgets.GTK.EditBox import CEditBox
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractEditBoxWithButton import CAbstractEditBoxWithButton

class CEditBoxWithButton(CAbstractEditBoxWithButton):
    
    def __init__(self,title):
        self.button=CButton(title)
        self.editbox=CEditBox(False)
        self.hbox=gtk.HBox()
        self.hbox.pack_start(self.editbox.GetWidget(),True,True)
        self.hbox.pack_start(self.button.GetWidget(),False,False,1)
        self.hbox.show()
    
    def GetWidget(self):
        return self.hbox
    
    def SetText(self,text):
        self.editbox.SetText(text)
    
    def GetText(self):
        return self.editbox.GetText()
    
    def SetHandler(self,event,func,data):
        if event=='clicked':
            self.button.SetHandler('clicked',func,data)
        if event=='changed':
            self.editbox.SetHandler('changed',func,data)