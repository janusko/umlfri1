from Widget import CWidget

class CButtonBar(CWidget):
    
    def GetItems(self): pass
    
    def AddButton(self, guiId, callback, position, label, imagefilename, tooglebutton): pass
        
    def AddStockButton(self, guiId, callback, position, stock, label, tooglebutton): pass
        
    def AddSeparator(self, guiId, position): pass
