from Widget import CWidget

class CButton(CWidget):
    
    def GetLabel(self):
        return self.obj.get_label()
    
    def SetLabel(self, value):
        self.obj.set_label(value)
    
    def ConnectClicked(self, callback):
        self.obj.connect('clicked', callback)
    
    def DisconnectClicked(self, callback):
        self.obj.disconnect('clicked', callback)
