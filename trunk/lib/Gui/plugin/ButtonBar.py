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
            
        self._addItem(guiId, callback, position, item)
    
    def _addSeparator(self, guiId, position):
        self._addItem(guiId, None, position, gtk.SeparatorToolItem())
    
    def AddButton(self, guiId, callback, position, label, imagefilename, tooglebutton):
        self._addButton(guiId, callback, position, None, label, imagefilename, tooglebutton)
        
    def AddStockButton(self, guiId, callback, position, stock, label, tooglebutton):
        self._addButton(guiId, callback, position, stock, label, None, tooglebutton)
        
    def AddSeparator(self, guiId, position):
        self._addSeparator(guiId, position)
    
