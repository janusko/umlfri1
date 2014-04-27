from MenuItem import CMenuItem

class CCheckMenuItem(CMenuItem):
    type = "toggle"
    
    def GetActive(self):
        return self.obj.get_active()
        
    def SetActive(self, value):
        self.obj.set_active(value)
        
    def GetInconsistent(self):
        return self.obj.get_inconsistent()
        
    def SetInconsistent(self, value):
        self.obj.set_inconsistent(value)
        
    def GetRadio(self):
        return self.obj.get_draw_as_radio()
        
    def SetRadio(self, value):
        self.obj.set_draw_as_radio(value)
