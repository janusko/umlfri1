from lib.Depend.gtk2 import gtk
from Widget import CWidget

class CContainer(CWidget):
    
    def AddItem(self, guiId, callback, position, item):
        if callback:
            if isinstance(item, gtk.MenuItem) and not isinstance(item, gtk.SeparatorMenuItem):
                item.connect('activate', callback)
            elif isinstance(item, gtk.ToolButton):
                item.connect('clicked', callback)
        item.set_name(guiId)
        item.show()
        if position < 0:
            position = max(0, len(self.obj.get_children()) + position + 1)
        self.obj.insert(item, position)
        
    def GetItems(self):
        for child in self.obj.get_children():
            yield self.manager.GetItem(child)
    
    def GetItem(self, guiId):
        for item in self.GetItems():
            if item.GetGuiId() == guiId:
                return item



