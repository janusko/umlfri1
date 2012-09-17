from Widget import CWidget

class CButtonBar(CWidget):
    _persistent = True
    
    def GetItems(self): pass
    
    def AddButton(self, guiId, callback, position, label, imagefilename, tooglebutton, _addr): pass
        
    def AddStockButton(self, guiId, callback, position, stock, label, tooglebutton, _addr): pass
        
    def AddSeparator(self, guiId, position, _addr): pass
