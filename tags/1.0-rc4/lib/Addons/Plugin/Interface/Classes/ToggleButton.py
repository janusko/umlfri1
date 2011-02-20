import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Button import IButton
from lib.Addons.Plugin.Communication.ComSpec import *

class IToggleButton(IButton):
    
    __cls__ = lib.GenericGui.CToggleButton
    
    def GetActive(him): 
        return him.GetActive()
        
    @mainthread
    def SetActive(him, value):
        him.SetActive(value)
