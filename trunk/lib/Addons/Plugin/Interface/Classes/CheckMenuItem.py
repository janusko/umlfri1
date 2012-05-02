import lib.GenericGui
from lib.Depend.gtk2 import gtk
from MenuItem import IMenuItem
from lib.Addons.Plugin.Communication.ComSpec import *

class ICheckMenuItem(IMenuItem):
    
    __cls__ = lib.GenericGui.CCheckMenuItem
    
    def GetActive(him):
        return him.GetActive()
        
    @mainthread
    def SetActive(him, value): 
        him.SetActive(value)
        
    def GetInconsistent(him):
        return him.GetInconsistent()
        
    @mainthread
    def SetInconsistent(him, value):
        him.SetInconsistent(value)
        
    def GetRadio(him):
        return him.GetRadio()
        
    @mainthread
    def SetRadio(him, value):
        him.SetRadio(value)
