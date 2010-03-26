import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Container import CContainer

class CMenu(CContainer, lib.GenericGui.CMenu):
    
    def _addMenuItem(self, callback, position, label, underline, imagefilename):
        if imagefilename:
            item = gtk.ImageMenuItem(label)
            image = gtk.Image()
            image.set_from_file(imagefilename)
            item.set_image(image)
        else:
            item = gtk.MenuItem(label, underline)
        self._addItem(callback, position, item)
        
    def _addStockMenuItem(self, callback, position, stock, label):
        item = gtk.ImageMenuItem(stock_id = stock)
        if label:
            item.set_label(label)
        self._addItem(callback, position, item)
        
    def _addCheckMenuItem(self, callback, position, label, underline):
        item = gtk.CheckMenuItem(label, underline)
        item.set_label(label)
        self._addItem(callback, position, item)
        
    def _addSeparator(self, position):
        self._addItem(None, position, gtk.SeparatorMenuItem())
    
    def AddMenuItem(self, callback, position, label, underline, imagefilename):
        gtk.idle_add(self._addMenuItem, callback, position, label, underline, imagefilename)
    
    def AddStockMenuItem(self, callback, position, stock, label):
        gtk.idle_add(self._addStockMenuItem, callback, position, stock, label)
    
    def AddCheckMenuItem(self, callback, position, label, underline):
        gtk.idle_add(self._addCheckMenuItem, callback, position, label, underline)
    
    def AddSeparator(self, position):
        gtk.idle_add(self._addSeparator, position)
    
