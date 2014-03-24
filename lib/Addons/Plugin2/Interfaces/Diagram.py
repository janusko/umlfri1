from .Decorators import params, mainthread, polymorphic

from lib.Commands.Diagrams import CCreateElementCommand

from lib.Drawing import CElement, CConnection, CConLabelInfo

from .DomainObject import IDomainObject

from . import ElementVisual
from . import ConnectionVisual
from . import DiagramType
from . import ConnectionLabel

class IDiagram(IDomainObject):
    def __init__(self, plugin, diagram):
        IDomainObject.__init__(self, plugin, diagram)
        
        self.__plugin = plugin
        self.__diagram = diagram
    
    @property
    def uid(self):
        return self.__diagram.GetUID()
    
    @property
    def _diagram(self):
        return self.__diagram
    
    def __castItem(self, item):
        if isinstance(item, CElement):
            return ElementVisual.IElementVisual(self.__plugin, item)
        elif isinstance(item, CConnection):
            return ConnectionVisual.IConnectionVisual(self.__plugin, item)
        elif isinstance(item, CConLabelInfo):
            return ConnectionLabel.IConnectionLabel(self.__plugin, item)
    
    @params(object)
    def GetElement(self, obj):
        element = self.__diagram.GetElement(obj._element)
        if element is None:
            return None
        return ElementVisual.IElementVisual(self.__plugin, )
    
    @params(object)
    def GetConnection(self, obj):
        connection = self.__diagram.GetConnection(obj._connection)
        if connection is None:
            return None
        return ConnectionVisual.IConnectionVisual(self.__plugin, )
    
    def GetType(self):
        return DiagramType.IDiagramType(self.__diagram.GetType())
    
    @polymorphic
    def GetSelected(self):
        for item in self.__diagram.GetSelected():
            yield self.__castItem(item)
    
    def GetSelectedElements(self):
        for item in self.__diagram.GetSelectedElements(True):
            yield ElementVisual.IElementVisual(self.__plugin, item)
        
    def GetSelectedConnectionLabels(self):
        for item in self.__diagram.GetSelectedElements(False):
            if isinstance(item, CConLabelInfo):
                yield ConnectionLabel.IConnectionLabel(self.__plugin, item)
    
    def GetSelectedConnections(self): 
        for item in self.__diagram.GetSelectedConnections():
            yield ConnectionVisual.IConnectionVisual(self.__plugin, item)
        
    def GetSelectSquare(self):
        return self.__diagram.GetSelectSquare()
    
    @polymorphic
    @params((int, int))
    def GetElementAtPosition(self, pos): 
        return self.__castItem(self.__diagram.GetElementAtPosition(pos))
    
    @params((int, int), (int, int), bool)
    def GetElementsInRange(self, topLeft, bottomRight, includeAll):
        for item in self.__diagram.GetElementsInRange(topLeft, bottomRight, includeAll):
            yield ElementVisual.IElementVisual(self.__plugin, item)
    
    def GetSizeSquare(self):
        return self.__diagram.GetSizeSquare()
    
    def GetElements(self):
        for item in self.__diagram.GetElements(True):
            yield ElementVisual.IElementVisual(self.__plugin, item)
        
    def GetConnections(self):
        for item in self.__diagram.GetConnections():
            yield ConnectionVisual.IConnectionVisual(self.__plugin, item)
    
    def GetName(self):
        return self.__diagram.GetName()
    
    def CreateElement(self, elementType):
        cmd = CCreateElementCommand(elementType._elementType, self.__diagram)
        self.__plugin.GetTransaction().Execute(cmd)
        return ElementVisual.IElementVisual(self.__plugin, cmd.GetElementVisual())
