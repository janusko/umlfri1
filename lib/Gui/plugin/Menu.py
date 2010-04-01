import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Container import CContainer

class CMenu(CContainer, lib.GenericGui.CMenu):
    
    def AddMenuItem(self, guiId, callback, position, label, underline, imagefilename):
        if imagefilename:
            item = gtk.ImageMenuItem(label)
            image = gtk.Image()
            image.set_from_file(imagefilename)
            item.set_image(image)
        else:
            item = gtk.MenuItem(label, underline)
        self.AddItem(guiId, callback, position, item)
        return self.manager.GetItem(item)
    
    def AddStockMenuItem(self, guiId, callback, position, stock, label):
        item = gtk.ImageMenuItem(stock_id = stock)
        if label:
            item.set_property('label', label)
        self.AddItem(guiId, callback, position, item)
        return self.manager.GetItem(item)
    
    def AddCheckMenuItem(self, guiId, callback, position, label, underline):
        item = gtk.CheckMenuItem(label, underline)
        item.set_property('label', label)
        self._addItem(guiId, callback, position, item)
        return self.manager.GetItem(item)
    
    def AddSeparator(self, guiId, position):
        item = gtk.SeparatorMenuItem()
        self.AddItem(guiId, None, position, item)
        return self.manager.GetItem(item)
    
