from base import IBase
from lib.GenericGui import CWidget
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IWidget(IBase):
    
    __cls__ = None
    
    @result(r_none)
    @parameter('value', t_bool)
    def SetSensitive(him, value):
        him.SetSensitive(value)
        
    @result(r_bool)
    def GetSensitive(him):
        return him.GetSensitive()
    
