from .Decorators import params, mainthread, polymorphic

class IConnectionVisual(object):
    def __init__(self, plugin, connection):
        self.__plugin = plugin
        self.__connection = connection
    
    @property
    def uid(self):
        return self.__connection.GetUID()
    
    @property
    def _connection(self):
        return self.__connection
    
    def GetObject(self):
        from . import ConnectionObject
        return ConnectionObject.IConnectionObject(self.__plugin, self.__connection.GetObject())
    
    def GetDestination(self):
        from . import ElementVisual
        
        return ElementVisual.IElementVisual(self.__plugin, self.__connection.GetDestination())
    
    def GetSource(self):
        from . import ElementVisual
        
        return ElementVisual.IElementVisual(self.__plugin, self.__connection.GetSource())
    
    def GetPoints(self):
        for point in self.__connection.GetPoints():
            yield point
    
    def GetAllLabelPositions(self):
        for point in self.__connection.GetAllLabelPositions():
            yield point
    
    def GetDiagram(self):
        from . import Diagram
        
        return Diagram.IDiagram(self.__plugin, self.__connection.GetDiagram())
