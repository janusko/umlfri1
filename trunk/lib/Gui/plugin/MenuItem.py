import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Widget import CWidget

class CMenuItem(lib.GenericGui.CMenuItem, CWidget):
    
    def GetLabel(self):
        return self.obj.get_property('label')
    
    def SetLabel(self, value):
        self.obj.set_property('label', value)
    
    def GetSubmenu(self):
        return self.manager.GetItem(self.obj.get_submenu())
    
    def AddSubmenu(self):
        menu = gtk.Menu()
        self.obj.set_submenu(menu)
        return self.manager.GetItem(menu)
        
