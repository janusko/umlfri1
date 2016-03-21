from .Decorators import params, mainthread, polymorphic

from .VisibleObject import IVisibleObject

from . import ConnectionObject

class IConnectionLabel(IVisibleObject):
    def __init__(self, plugin, label):
        IVisibleObject.__init__(self, plugin, label)
        
        self.__plugin = plugin
        self.__label = label
    
    @property
    def uid(self):
        return self.__label.GetUID()
    
    def GetObject(self):
        return ConnectionObject.IConnectionObject(self.__plugin, self.__label.GetObject())
