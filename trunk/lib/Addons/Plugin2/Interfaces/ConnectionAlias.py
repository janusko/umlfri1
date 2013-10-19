from .Decorators import params, mainthread, polymorphic

from .ConnectionType import IConnectionType

class IConnectionAlias(IConnectionType):
    def __init__(self, alias):
        IConnectionType.__init__(self, alias)
        
        self.__alias = alias
    
    def GetAlias(self):
        return self.__alias.GetAlias()
