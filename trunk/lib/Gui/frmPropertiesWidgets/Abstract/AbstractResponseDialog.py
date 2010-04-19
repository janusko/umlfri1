class CAbstractResponseDialog(object):
    
    def __init__(self,title=''):
        pass
    
    def GetWidget(self):
        pass
    
    def Show(self):
        pass
    
    def Close(self):
        pass
    
    def SetQuestion(self,question):
        pass
    
    def SetToggleButton(self,button):
        pass
    
    def AppendResponse(self,response,name,default=False):
        pass
    