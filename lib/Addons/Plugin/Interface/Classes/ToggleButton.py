import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Button import IButton
from lib.Addons.Plugin.Communication.ComSpec import *

class IToggleButton(IButton):
    
    __cls__ = lib.GenericGui.CToggleButton
    
    @result(r_bool)
    def GetActive(him): 
        return him.GetActive()
        
    @result(r_none)
    @parameter('value', t_bool)
    @mainthread
    def SetActive(him, value):
        him.SetActive(value)
