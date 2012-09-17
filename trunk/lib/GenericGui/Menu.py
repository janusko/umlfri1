from Widget import CWidget

class CMenu(CWidget):
    _persistent = True
    
    def GetItems(self):
        pass
        
    def AddMenuItem(self, guiId, callback, position, label, underline, imagefilename, _addr):
        pass
    
    def AddStockMenuItem(self, guiId, callback, position, stock, label, _addr):
        pass
    
    def AddCheckMenuItem(self, guiId, callback, position, label, underline, _addr):
        pass
    
    def AddSeparator(self, guiId, position, _addr):
        pass
