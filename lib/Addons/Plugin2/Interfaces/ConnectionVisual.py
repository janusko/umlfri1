from .Decorators import params, mainthread, polymorphic

from . import ConnectionObject
from . import ElementVisual
from . import Diagram

class IConnectionVisual(object):
    def __init__(self, plugin, connection):
        self.__plugin = plugin
        self.__connection = connection
    
    @property
    def _connection(self):
        return self.__connection
    
    def GetObject(self):
        return ConnectionObject.IConnectionObject(self.__plugin, self.__connection.GetObject())
    
    def GetDestination(self):
        return ElementVisual.IElementVisual(self.__plugin, self.__connection.GetDestination())
    
    def GetSource(self):
        return ElementVisual.IElementVisual(self.__plugin, self.__connection.GetSource())
    
    def GetPoints(self):
        for point in self.__connection.GetPoints():
            yield point
    
    def GetAllLabelPositions(self):
        for point in self.__connection.GetAllLabelPositions():
            yield point
    
    def GetDiagram(self):
        return Diagram.IDiagram(self.__plugin, self.__connection.GetDiagram())
