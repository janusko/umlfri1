from Widget import IWidget
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IContainer(IWidget):
    __cls__ = None
    
    def GetItems(him):
        return list(him.GetItems())
    
    def GetItem(him, guiId):
        return him.GetItem(guiId)
    
    
