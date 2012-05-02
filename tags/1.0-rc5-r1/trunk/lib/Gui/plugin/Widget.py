import lib.GenericGui
from lib.Depend.gtk2 import gtk

class CWidget(lib.GenericGui.CWidget):
    
    def __init__(self, obj, manager, guiId, owner):
        self.obj = obj
        self.manager = manager
        self.owner = owner
        self._guiId = guiId
        self._persistent = True
        
    def GetGuiId(self):
        return self._guiId
        
    def SetSensitive(self, value):
        self.obj.set_property('sensitive', value)
        
    def GetSensitive(self):
        return self.obj.get_property('sensitive')
    
    def GetVisible(self):
        return self.obj.get_property('visible')
    
    def SetVisible(self, value):
        if value:
            self.obj.show()
        else:
            self.obj.hide()
    
    def GetObject(self):
        return self.obj
    
    def TestAccess(self, addr):
        if self.owner is not None and self.owner != addr:
            raise PluginAccessDenied()
            
    def Remove(self):
        if self.obj is not None and self.obj.parent is not None:
            self.obj.parent.remove(self.obj)
        self.obj = None
        
    def Hide(self):
        if self.obj is not None:
            self.obj.hide()
        
    def Show(self):
        if self.obj is not None:
            self.obj.show()
    
