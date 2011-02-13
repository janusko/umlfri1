import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Widget import IWidget
from lib.Addons.Plugin.Communication.ComSpec import *

class IMenuItem(IWidget):
    __cls__ = lib.GenericGui.CMenuItem
    
    def GetSubmenu(him):
        return him.GetSubmenu()
        
    def GetLabel(him):
        return him.GetLabel()
        
    @mainthread
    def SetLabel(him, value):
        him.SetLabel(value)
        
    @mainthread
    @includeAddr
    def AddSubmenu(him, _addr=None):
        return him.AddSubmenu(_addr)
        
