from Widget import IWidget
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IContainer(IWidget):
    __cls__ = None
    
    @result(r_objectlist)
    def GetItems(him):
        return list(him.GetItems())
    
    @result(r_object)
    @parameter('guiId', t_str)
    def GetItem(him, guiId):
        return him.GetItem(guiId)
    
    
