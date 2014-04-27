from lib.Depend.gtk2 import gtk
from Widget import CWidget
from lib.Exceptions import *

class CMenuItem(CWidget):
    
    def GetLabel(self):
        return self.obj.get_property('label')
    
    def SetLabel(self, value):
        self.obj.set_property('label', value)
    
    def GetSubmenu(self):
        return self.manager.GetItem(self.obj.get_submenu())
    
    def AddSubmenu(self, _addr):
        if self.obj.get_submenu() is not None:
            raise PluginAccessDenied()
        self.TestAccess(_addr)
        menu = gtk.Menu()
        self.obj.set_submenu(menu)
        return self.manager.GetItem(menu, _addr)
    
    def ConnectClicked(self, callback):
        self.obj.connect('activate', callback)
    
    def DisconnectClicked(self, callback):
        self.obj.disconnect('activate', callback)
