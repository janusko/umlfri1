import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Container import CContainer

class CButtonBar(CContainer, lib.GenericGui.CButtonBar):
    
    def _addButton(self, guiId, callback, position, stock, label, imagefilename, tooglebutton, _addr):
        self.TestAccess(_addr)
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
        
        return self.manager.GetItem(item, _addr)
    
    def AddButton(self, guiId, callback, position, label, imagefilename, tooglebutton, _addr):
        return self._addButton(guiId, callback, position, None, label, imagefilename, tooglebutton, _addr)
        
    def AddStockButton(self, guiId, callback, position, stock, label, tooglebutton, _addr):
        return self._addButton(guiId, callback, position, stock, label, None, tooglebutton, _addr)
        
    def AddSeparator(self, guiId, position, _addr):
        self.TestAccess(_addr)
        item = gtk.SeparatorToolItem()
        self.AddItem(guiId, None, position, item)
        return self.manager.GetItem(item, _addr)
    
