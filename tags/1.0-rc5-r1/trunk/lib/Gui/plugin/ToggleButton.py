import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Button import CButton

class CToggleButton(lib.GenericGui.CToggleButton, CButton):
    
    def GetActive(self): 
        return self.obj.get_active()
        
    def SetActive(self, value):
        return self.obj.set_active(value)
