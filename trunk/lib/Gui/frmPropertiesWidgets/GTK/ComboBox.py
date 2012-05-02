import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractComboBox import CAbstractComboBox

class CComboBox(CAbstractComboBox):
    
    def __init__(self):
        self.combobox=gtk.combo_box_new_text()
        self.combobox.show()
    
    def GetWidget(self):
        return self.combobox
    
    def AppendItem(self,item):
        self.combobox.append_text(item)
    
    def SetActiveItem(self,idx):
        self.combobox.set_active(idx)
    
    def SetActiveItemText(self,text):
        model=self.combobox.get_model()
        iter=model.get_iter('0')
        tmp=[]
        while iter!=None:
            tmp.append(model.get_value(iter,0))
            iter=model.iter_next(iter)
        self.combobox.set_active(tmp.index(str(text)))
    
    def GetActiveItemText(self):
        return self.combobox.get_active_text()
    
    def SetHandler(self,event,func,data=None):
        if event=='changed':
            self.combobox.connect('changed',self.__ComboBoxEventHandler,func,data)
    
    def __ComboBoxEventHandler(self,combobox,func,data=None):
        if data!=None:
            func(*data)
        else:
            func()