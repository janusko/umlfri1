import lib.GenericGui
from lib.Depend.gtk2 import gtk
from Widget import IWidget
from lib.Addons.Plugin.Communication.ComSpec import *

class IButton(IWidget):
    
    __cls__ = lib.GenericGui.CButton
    
    def GetLabel(him):
        return him.GetLabel()
    
    @mainthread
    def SetLabel(him, value):
        him.SetLabel(value)
    
