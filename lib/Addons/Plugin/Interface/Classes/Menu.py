from Container import IContainer
from lib.GenericGui import CMenu
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IMenu(IContainer):
    __cls__ = CMenu
    
    @mainthread
    @includeAddr
    def AddMenuItem(him, guiId, callback, position, label, underline=True, imagefilename=None, _addr=None):
        return him.AddMenuItem(guiId, callback, position, label, underline, imagefilename, _addr)
    
    @mainthread
    @includeAddr
    def AddStockMenuItem(him, guiId, callback, position, stock, label=None, _addr=None):
        return him.AddStockMenuItem(guiId, callback, position, stock, label, _addr)
    
    @mainthread
    @includeAddr
    def AddCheckMenuItem(him, guiId, callback, position, label, underline=True, _addr=None):
        return him.AddCheckMenuItem(guiId, callback, position, label, underline, _addr)
    
    @mainthread
    @includeAddr
    def AddSeparator(him, guiId, position, _addr=None):
        return him.AddSeparator(guiId, position, _addr)

