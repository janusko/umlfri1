class CAbstractTable(object):
    
    def __init__(self,model,delete,save,new):
        pass
    
    def GetWidget(self):
        pass
    
    def Clear(self):
        pass
    
    def AppendRow(self,data,row_object):
        pass
    
    def RemoveRow(self,idx):
        pass
    
    def GetRowObject(self,idx):
        pass
    
    def GetAllRowObjects(self):
        pass
    
    def SetCellValue(self,row,col,value):
        pass
    
    def GetSelectedRowIndex(self):
        pass
    
    def UnselectAll(self):
        pass
    
    def SetHandler(self,event,func,data):
        pass
    