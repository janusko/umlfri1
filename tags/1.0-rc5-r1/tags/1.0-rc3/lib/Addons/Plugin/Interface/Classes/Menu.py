from Container import IContainer
from lib.GenericGui import CMenu
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IMenu(IContainer):
    __cls__ = CMenu
    
    @result(r_object)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('underline', t_bool)
    @parameter('imagefilename', t_str)
    @mainthread
    @includeAddr
    def AddMenuItem(him, guiId, callback, position, label, underline=True, imagefilename=None, _addr=None):
        return him.AddMenuItem(guiId, callback, position, label, underline, imagefilename, _addr)
    
    @result(r_object)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('stock', t_str)
    @parameter('label', t_str)
    @mainthread
    @includeAddr
    def AddStockMenuItem(him, guiId, callback, position, stock, label=None, _addr=None):
        return him.AddStockMenuItem(guiId, callback, position, stock, label, _addr)
    
    @result(r_object)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('underline', t_bool)
    @mainthread
    @includeAddr
    def AddCheckMenuItem(him, guiId, callback, position, label, underline=True, _addr=None):
        return him.AddCheckMenuItem(guiId, callback, position, label, underline, _addr)
    
    @result(r_object)
    @parameter('guiId', t_str)
    @parameter('position', t_int)
    @mainthread
    @includeAddr
    def AddSeparator(him, guiId, position, _addr=None):
        return him.AddSeparator(guiId, position, _addr)

