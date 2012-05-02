from ElementType import IElementType
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Elements import CElementAlias

class IElementAlias(IElementType):
    
    __cls__ = CElementAlias
    
    @result(r_str)
    def GetAlias(him):
        return him.GetAlias()
