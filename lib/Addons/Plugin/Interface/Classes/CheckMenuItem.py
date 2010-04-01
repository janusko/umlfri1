import lib.GenericGui
from lib.Depend.gtk2 import gtk
from MenuItem import IMenuItem
from lib.Addons.Plugin.Communication.ComSpec import *

class ICheckMenuItem(IMenuItem):
    
    __cls__ = lib.GenericGui.CCheckMenuItem
    
    @result(r_bool)
    def GetActive(him):
        return him.GetActive()
        
    @result(r_none)
    @parameter('value', t_bool)
    @mainthread
    def SetActive(him, value): 
        him.SetActive(value)
        
    @result(r_bool)
    def GetInconsistent(him):
        return him.GetInconsistent()
        
    @result(r_none)
    @parameter('value', t_bool)
    @mainthread
    def SetInconsistent(him, value):
        him.SetInconsistent(value)
        
    @result(r_bool)
    def GetRadio(him):
        return him.GetRadio()
        
    @result(r_none)
    @parameter('value', t_bool)
    @mainthread
    def SetRadio(him, value):
        him.SetRadio(value)
