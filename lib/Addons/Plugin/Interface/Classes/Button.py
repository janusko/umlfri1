import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Widget import IWidget
from lib.Addons.Plugin.Communication.ComSpec import *

class IButton(IWidget):
    
    __cls__ = lib.GenericGui.CButton
    
    @result(r_str)
    def GetLabel(him):
        return him.GetLabel()
    
    @result(r_none)
    @parameter('value', t_str)
    def SetLabel(him, value):
        return him.SetLabel(value)
    
