from ..PluginBase import params, mainthread, polymorphic

from . import Diagram

class IVisibleObject(object):
    def __init__(self, plugin, object):
        self.__plugin = plugin
        self.__object = object
    
    def GetPosition(self):
        return self.__object.GetPosition(self.__plugin.GetCanvas())
    
    def GetCenter(self):
        return self.__object.GetCenter(self.__plugin.GetCanvas())
    
    def GetSize(self):
        return self.__object.GetSize(self.__plugin.GetCanvas())
    
    def GetMinimalSize(self):
        return self.__object.GetMinimalSize(self.__plugin.GetCanvas())
    
    def GetSquare(self):
        return self.__object.GetSquare(self.__plugin.GetCanvas())
    
    @params((int, int))
    def AreYouAtPosition(self, pos):
        return self.__object.AreYouAtPosition(self.__plugin.GetCanvas(), pos)
    
    @params((int, int), (int, int), bool)
    def AreYouInRange(self, topLeft, bottomRight, includeAll):
        return self.__object.AreYouInRange(self.__plugin.GetCanvas(), topLeft, bottomRight, includeAll)
    
    def GetDiagram(self):
        return Diagram.IDiagram(self.__plugin, self.__object.GetDiagram())
