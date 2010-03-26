import lib.GenericGui
from lib.Depend.gtk2 import gtk

class CWidget(lib.GenericGui.CWidget):
    
    def __init__(self, obj, manager):
        self.obj = obj
        self.manager = manager
        
    def SetSensitive(self, value):
        gtk.idle_add(self.obj.set_property, 'sensitive', value)
        
    def GetSensitive(self):
        return self.obj.get_property('sensitive')
    
