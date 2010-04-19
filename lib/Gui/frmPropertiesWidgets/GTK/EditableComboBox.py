import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractEditableComboBox import CAbstractEditableComboBox

class CEditableComboBox(CAbstractEditableComboBox):
    
    def __init__(self):
        self.combobox=gtk.combo_box_entry_new_text()
        self.combobox.show()
    
    def GetWidget(self):
        return self.combobox
    
    def AppendItem(self,item):
        self.combobox.append_text(item)
    
    def SetActiveItemText(self,text):
        self.combobox.set_active(-1)
        self.combobox.get_child().set_text(text)
    
    def GetActiveItemText(self):
        return self.combobox.get_active_text()
    
    def SetHandler(self,event,func,data=None):
        if event=='changed':
            self.combobox.connect('changed',self.__EditableComboBoxEventHandler,func,data)
    
    def __EditableComboBoxEventHandler(self,combobox,func,data=None):
        if data!=None:
            func(*data)
        else:
            func()