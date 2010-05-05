class CAbstractDialog(object):
    
    def __init__(self,parent,title=''):
        pass
    
    def GetWidget(self):
        return self.dialog
    
    def SetTitle(self,title):
        pass
    
    def GetTitle(self):
        pass
    
    def SetSize(self,x,y):
        pass
    
    def GetSize(self):
        pass
    
    def Close(self):
        pass
    
    def Show(self):
        pass
    
    def AppendButton(self,button):
        pass
    
    def AppendTab(self,title):
        pass
    
    def SetCurrentTab(self,idx):
        pass
    
    def AppendItemToTab(self,tabname,item,itemname):
        pass
    
    def SetHandler(self,event,func,data):
        pass
    
    def GrabFirst(self):
        pass
    