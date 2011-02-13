import lib.GenericGui
from lib.Depend.gtk2 import gtk
from MenuItem import IMenuItem
from lib.Addons.Plugin.Communication.ComSpec import *

class IImageMenuItem(IMenuItem):
    
    __cls__ = lib.GenericGui.CImageMenuItem
    
    @mainthread
    def SetImageFromFile(him, filename):
        him.SetImageFromFile(filename)
