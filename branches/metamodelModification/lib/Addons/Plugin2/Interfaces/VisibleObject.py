from .Decorators import params, mainthread, polymorphic

class IVisibleObject(object):
    def __init__(self, plugin, object):
        self.__plugin = plugin
        self.__object = object
    
    def GetPosition(self):
        return self.__object.GetPosition()
    
    def GetCenter(self):
        return self.__object.GetCenter()
    
    def GetSize(self):
        return self.__object.GetSize()
    
    def GetMinimalSize(self):
        return self.__object.GetMinimalSize()
    
    def GetSquare(self):
        return self.__object.GetSquare()
    
    @params((int, int))
    def AreYouAtPosition(self, pos):
        return self.__object.AreYouAtPosition(pos)
    
    @params((int, int), (int, int), bool)
    def AreYouInRange(self, topLeft, bottomRight, includeAll):
        return self.__object.AreYouInRange(topLeft, bottomRight, includeAll)
    
    def GetDiagram(self):
        from . import Diagram
        
        return Diagram.IDiagram(self.__plugin, self.__object.GetDiagram())
