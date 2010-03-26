from Widget import CWidget

class CMenu(CWidget):
    
    def GetItems(self):
        pass
        
    def AddMenuItem(self, callback, position, label, underline, imagefilename):
        pass
    
    def AddStockMenuItem(self, callback, position, stock, label):
        pass
    
    def AddCheckMenuItem(self, callback, position, label, underline):
        pass
    
    def AddSeparator(self, position):
        pass
