import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Widget import CWidget

class CMenuItem(lib.GenericGui.CMenuItem, CWidget):
    
    def GetLabel(self):
        return self.obj.get_label()
    
    def SetLabel(self, value):
        gtk.idle_add(self.obj.set_label, value)
    
    def GetSubmenu(self):
        return self.manager.GetItem(self.obj.get_submenu())
    
    def AddSubmenu(self):
        menu = gtk.Menu()
        gtk.idle_add(self.obj.set_submenu, menu)
