import lib.GenericGui
from lib.Depend.gtk2 import gtk
from MenuItem import IMenuItem
from lib.Addons.Plugin.Communication.ComSpec import *

class IImageMenuItem(IMenuItem):
    
    __cls__ = lib.GenericGui.CImageMenuItem
    
    @mainthread
    @includeAddr
    def SetImageFromFile(him, filename, _addr=None):
        if filename is not None:
            filename = IImageMenuItem.RelativePath2Absolute(_addr, filename)
        him.SetImageFromFile(filename)
