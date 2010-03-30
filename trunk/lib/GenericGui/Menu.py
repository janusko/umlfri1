from Widget import CWidget

class CMenu(CWidget):
    
    def GetItems(self):
        pass
        
    def AddMenuItem(self, guiId, callback, position, label, underline, imagefilename):
        pass
    
    def AddStockMenuItem(self, guiId, callback, position, stock, label):
        pass
    
    def AddCheckMenuItem(self, guiId, callback, position, label, underline):
        pass
    
    def AddSeparator(self, guiId, position):
        pass
