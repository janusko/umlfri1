import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Widget import CWidget

class CButton(lib.GenericGui.CButton, CWidget):
    
    def GetLabel(self):
        return self.obj.get_label()
    
    def SetLabel(self, value):
        self.obj.set_label(value)
    