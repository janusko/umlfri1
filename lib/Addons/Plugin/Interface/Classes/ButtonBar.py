from Widget import IWidget
from lib.GenericGui import CButtonBar
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IButtonBar(IWidget):
    
    __cls__ = CButtonBar
    
    @result(r_objectlist)
    def GetItems(him):
        return list(him.GetItems())
    
    @result(r_none)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('imagefilename', t_str)
    @parameter('togglebutton', t_bool)
    def AddButton(him, guiId, callback, position, label, imagefilename=None, togglebutton=False):
        return him.AddButton(guiId, callback, position, label, imagefilename, togglebutton)
        
    @result(r_none)
    @parameter('guiId', t_str)
    @parameter('callback', t_callback)
    @parameter('stock', t_str)
    @parameter('position', t_int)
    @parameter('label', t_str)
    @parameter('togglebutton', t_bool)
    def AddStockButton(him, guiId, callback, position, stock, label=None, togglebutton=False):
        return him.AddStockButton(guiId, callback, position, stock, label, togglebutton)
    
    @result(r_none)
    @parameter('guiId', t_str)
    @parameter('position', t_int)
    def AddSeparator(him, guiId, position):
        him.AddSeparator(guiId, position)
