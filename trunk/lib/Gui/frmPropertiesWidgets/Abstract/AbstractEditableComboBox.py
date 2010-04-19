class CAbstractEditableComboBox(object):
    
    def GetWidget(self):
        pass
    
    def AppendItem(self,item):
        pass
    
    def SetActiveItemText(self,text):
        pass
    
    def GetActiveItemText(self):
        pass
    
    def SetHandler(self,event,func,data=None):
        pass
    