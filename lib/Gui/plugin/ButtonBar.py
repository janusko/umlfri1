import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Container import CContainer

class CButtonBar(CContainer, lib.GenericGui.CButtonBar):
    
    def _addButton(self, callback, position, stock, label, imagefilename, tooglebutton):
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
            
        self._addItem(callback, position, item)
    
    def _addSeparator(self, position):
        self._addItem(None, position, gtk.SeparatorToolItem())
    
    def AddButton(self, callback, position, label, imagefilename, tooglebutton):
        gtk.idle_add(self._addButton, callback, position, None, label, imagefilename, tooglebutton)
        
    def AddStockButton(self, callback, position, stock, label, tooglebutton):
        gtk.idle_add(self._addButton, callback, position, stock, label, None, tooglebutton)
        
    def AddSeparator(self, position):
        gtk.idle_add(self._addSeparator, position)
    
