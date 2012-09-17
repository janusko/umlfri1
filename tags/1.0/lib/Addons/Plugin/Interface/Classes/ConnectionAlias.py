from ConnectionType import IConnectionType
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Connections import CConnectionAlias

class IConnectionAlias(IConnectionType):
    
    __cls__ = CConnectionAlias
    
    def GetAlias(him):
        return him.GetAlias()
