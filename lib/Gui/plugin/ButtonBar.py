import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Container import CContainer

class CButtonBar(CContainer, lib.GenericGui.CButtonBar):
    
    def _addButton(self, guiId, callback, position, stock, label, imagefilename, tooglebutton):
        if tooglebutton:
            item = gtk.ToggleToolButton(stock)
        else:
            item = gtk.ToolButton(stock)
        
        if label:
            item.set_label(label)
        
        if imagefilename:
            image = gtk.Image()
            image.set_from_file(imagefilename)
            image.show()
            item.set_icon_widget(image)
            
        self.AddItem(guiId, callback, position, item)
        
        return self.manager.GetItem(item)
    
    def AddButton(self, guiId, callback, position, label, imagefilename, tooglebutton):
        return self._addButton(guiId, callback, position, None, label, imagefilename, tooglebutton)
        
    def AddStockButton(self, guiId, callback, position, stock, label, tooglebutton):
        return self._addButton(guiId, callback, position, stock, label, None, tooglebutton)
        
    def AddSeparator(self, guiId, position):
        item = gtk.SeparatorToolItem()
        self.AddItem(guiId, None, position, item)
        return self.manager.GetItem(item)
    
