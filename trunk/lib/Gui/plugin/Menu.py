import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Container import CContainer

class CMenu(CContainer, lib.GenericGui.CMenu):
    
    def _addMenuItem(self, guiId, callback, position, label, underline, imagefilename):
        if imagefilename:
            item = gtk.ImageMenuItem(label)
            image = gtk.Image()
            image.set_from_file(imagefilename)
            item.set_image(image)
        else:
            item = gtk.MenuItem(label, underline)
        self._addItem(guiId, callback, position, item)
        
    def _addStockMenuItem(self, guiId, callback, position, stock, label):
        item = gtk.ImageMenuItem(stock_id = stock)
        if label:
            item.set_property('label', label)
        self._addItem(guiId, callback, position, item)
        
    def _addCheckMenuItem(self, guiId, callback, position, label, underline):
        item = gtk.CheckMenuItem(label, underline)
        item.set_property('label', label)
        self._addItem(guiId, callback, position, item)
        
    def _addSeparator(self, guiId, position):
        self._addItem(guiId, None, position, gtk.SeparatorMenuItem())
    
    def AddMenuItem(self, guiId, callback, position, label, underline, imagefilename):
        self._addMenuItem(guiId, callback, position, label, underline, imagefilename)
    
    def AddStockMenuItem(self, guiId, callback, position, stock, label):
        self._addStockMenuItem(guiId, callback, position, stock, label)
    
    def AddCheckMenuItem(self, guiId, callback, position, label, underline):
        self._addCheckMenuItem(guiId, callback, position, label, underline)
    
    def AddSeparator(self, guiId, position):
        self._addSeparator(guiId, position)
    
