from Widget import CWidget

class CContainer(CWidget):
    
    def AddItem(self, guiId, position, item):
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
                
    def RenameStock(self, name):
        if isinstance(name, (str, unicode)):
            if not name.startswith('gtk-'):
                return 'gtk-' + name
        return name



