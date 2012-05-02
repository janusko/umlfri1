from base import IBase
from lib.GenericGui import CWidget
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IWidget(IBase):
    
    __cls__ = None
    
    def GetGuiId(him):
        return him.GetGuiId()
    
    @mainthread
    def SetEnabled(him, value):
        him.SetSensitive(value)
        
    def GetEnabled(him):
        return him.GetSensitive()
    
    def GetVisible(him):
        return him.GetVisible()
        
    def SetVisible(him, value):
        him.SetVisible(value)
    
