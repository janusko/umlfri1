from Container import IContainer
from lib.GenericGui import CButtonBar
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IButtonBar(IContainer):
    
    __cls__ = CButtonBar
    
    @result(r_object)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('imagefilename', t_str)
    @parameter('togglebutton', t_bool)
    @mainthread
    def AddButton(him, guiId, callback, position, label, imagefilename=None, togglebutton=False):
        return him.AddButton(guiId, callback, position, label, imagefilename, togglebutton)
        
    @result(r_object)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('stock', t_str)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('togglebutton', t_bool)
    @mainthread
    def AddStockButton(him, guiId, callback, position, stock, label=None, togglebutton=False):
        return him.AddStockButton(guiId, callback, position, stock, label, togglebutton)
    
    @result(r_object)
    @parameter('guiId', t_str)
    @parameter('position', t_int)
    @mainthread
    def AddSeparator(him, guiId, position):
        return him.AddSeparator(guiId, position)
