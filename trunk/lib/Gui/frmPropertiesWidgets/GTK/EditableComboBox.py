import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractEditableComboBox import CAbstractEditableComboBox

class CEditableComboBox(CAbstractEditableComboBox):
    
    def __init__(self,style='text'):
        self.combobox=gtk.combo_box_entry_new_text()
        if style=='int' or style=='float':
            self.combobox.get_child().connect('key-press-event',self.__EditableComboBoxHandler,style)
        self.lastkey=-1
        self.combobox.show()
    
    def GetWidget(self):
        return self.combobox
    
    def SetBackgroundColor(self,color):
        self.combobox.get_child().modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))
    
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
    
    def __EditableComboBoxHandler(self,entry,event,style):
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