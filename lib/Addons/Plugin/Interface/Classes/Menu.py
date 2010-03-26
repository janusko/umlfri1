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
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('underline', t_bool)
    @parameter('imagefilename', t_str)
    def AddMenuItem(him, callback, position, label, underline, imagefilename):
        return him.AddMenuItem(callback, position, label, underline, imagefilename)
    
    @result(r_none)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('stock', t_str)
    @parameter('label', t_str)
    def AddStockMenuItem(him, callback, position, stock, label):
        return him.AddStockMenuItem(callback, position, stock, label)
    
    @result(r_none)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('underline', t_bool)
    def AddCheckMenuItem(him, callback, position, label, underline):
        return him.AddCheckMenuItem(callback, position, label, underline)
    
    @result(r_none)
    @parameter('position', t_int)
    def AddSeparator(him, position):
        return him.AddSeparator(position)

