import lib.GenericGui
from lib.Depend.gtk2 import gtk

class CWidget(lib.GenericGui.CWidget):
    
    def __init__(self, obj, manager, guiId):
        self.obj = obj
        self.manager = manager
        self._guiId = guiId
        
    def GetGuiId(self):
        return self._guiId
        
    def SetSensitive(self, value):
        self.obj.set_property('sensitive', value)
        
    def GetSensitive(self):
        return self.obj.get_property('sensitive')
    
