import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Widget import IWidget
from lib.Addons.Plugin.Communication.ComSpec import *

class IMenuItem(IWidget):
    __cls__ = lib.GenericGui.CMenuItem
    
    @result(r_object)
    def GetSubmenu(him):
        return him.GetSubmenu()
        
    @result(r_str)
    def GetLabel(him):
        return him.GetLabel()
        
    @result(r_none)
    @parameter('value', t_str)
    def SetLabel(him, value):
        return him.SetLabel(value)
        
    @result(r_none)
    def AddSubmenu(him):
        him.AddSubmenu()
        
