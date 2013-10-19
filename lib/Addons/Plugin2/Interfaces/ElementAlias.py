from ..PluginBase import params, mainthread, polymorphic

from .ElementType import IElementType

class IElementAlias(IElementType):
    def __init__(self, elementAlias):
        IElementType.__init__(self, elementAlias)
        
        self.__elementAlias = elementAlias
    
    def GetAlias(self):
        return self.__elementAlias.GetAlias()
