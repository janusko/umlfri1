from lib.Depend.gtk2 import gtk
from Widget import CWidget

class CContainer(CWidget):
    
    def _addItem(self, callback, position, item):
        if callback:
            if isinstance(item, gtk.MenuItem):
                item.connect('activate', callback)
            elif isinstance(item, gtk.ToolButton):
                item.connect('clicked', callback)
        item.show()
        self.obj.insert(item, position)
        
    def GetItems(self):
        for child in self.obj.get_children():
            yield self.manager.GetItem(child)



