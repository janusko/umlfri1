from lib.Depend.gtk2 import gtk
from Container import CContainer

class CMenu(CContainer):
    
    def AddMenuItem(self, guiId, callback, position, label, underline, imagefilename, _addr):
        self.TestAccess(_addr)
        
        if imagefilename:
            item = gtk.ImageMenuItem(label)
            image = gtk.Image()
            image.set_from_file(imagefilename)
            item.set_image(image)
        else:
            item = gtk.MenuItem(label, underline)
        self.AddItem(guiId, callback, position, item)
        return self.manager.GetItem(item, _addr)
    
    def AddStockMenuItem(self, guiId, position, stock, label, _addr):
        self.TestAccess(_addr)
        stock = self.RenameStock(stock)
        item = gtk.ImageMenuItem(stock_id = stock)
        if label:
            item.set_property('label', label)
        self.AddItem(guiId, position, item)
        return self.manager.GetItem(item, _addr)
    
    def AddCheckMenuItem(self, guiId, position, label, underline, _addr):
        self.TestAccess(_addr)
        item = gtk.CheckMenuItem(label, underline)
        item.set_property('label', label)
        self._addItem(guiId, position, item)
        return self.manager.GetItem(item, _addr)
    
    def AddSeparator(self, guiId, position, _addr):
        self.TestAccess(_addr)
        item = gtk.SeparatorMenuItem()
        self.AddItem(guiId, None, position, item)
        return self.manager.GetItem(item, _addr)
    
