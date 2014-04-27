from Button import CButton

class CToggleButton(CButton):
    
    def GetActive(self): 
        return self.obj.get_active()
        
    def SetActive(self, value):
        return self.obj.set_active(value)
