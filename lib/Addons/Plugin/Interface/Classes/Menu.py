from Widget import IWidget
from lib.GenericGui import CMenu
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IMenu(IWidget):
    __cls__ = CMenu
    
    @result(r_objectlist)
    def GetItems(him):
        return list(him.GetItems())
    
    @result(r_none)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('underline', t_bool)
    @parameter('imagefilename', t_str)
    def AddMenuItem(him, guiId, callback, position, label, underline=True, imagefilename=None):
        return him.AddMenuItem(guiId, callback, position, label, underline, imagefilename)
    
    @result(r_none)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('stock', t_str)
    @parameter('label', t_str)
    def AddStockMenuItem(him, guiId, callback, position, stock, label=None):
        return him.AddStockMenuItem(guiId, callback, position, stock, label)
    
    @result(r_none)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('underline', t_bool)
    def AddCheckMenuItem(him, guiId, callback, position, label, underline=True):
        return him.AddCheckMenuItem(guiId, callback, position, label, underline)
    
    @result(r_none)
    @parameter('guiId', t_str)
    @parameter('position', t_int)
    def AddSeparator(him, guiId, position):
        return him.AddSeparator(guiId, position)

