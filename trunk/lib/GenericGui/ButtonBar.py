from Widget import CWidget

class CButtonBar(CWidget):
    
    def GetItems(self): pass
    
    def AddButton(self, callback, position, label, imagefilename, tooglebutton): pass
        
    def AddStockButton(self, callback, position, stock, label, tooglebutton): pass
        
    def AddSeparator(self, position): pass
