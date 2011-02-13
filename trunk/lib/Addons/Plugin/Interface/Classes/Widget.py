from base import IBase
from lib.GenericGui import CWidget
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IWidget(IBase):
    
    __cls__ = None
    
    def GetGuiId(him):
        return him.GetGuiId()
    
    @mainthread
    def SetSensitive(him, value):
        him.SetSensitive(value)
        
    def GetSensitive(him):
        return him.GetSensitive()
    
