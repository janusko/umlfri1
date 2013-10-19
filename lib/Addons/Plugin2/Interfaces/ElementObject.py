from .Decorators import params, mainthread, polymorphic

from DomainObject import IDomainObject

from lib.Commands.Diagrams import CShowElementCommand
from lib.Commands.Project import CCreateConnectionObjectCommand, CCreateDiagramCommand, CCreateElementObjectCommand
from lib.Elements import CElementAlias, CElementType
from lib.Exceptions import PluginInvalidMethodParameters

from . import ElementAlias
from . import ElementType
from . import Diagram
from . import ConnectionObject
from . import ElementVisual

class IElementObject(IDomainObject):
    def __init__(self, plugin, element):
        IDomainObject.__init__(self, plugin, element)
        
        self.__plugin = plugin
        self.__element = element
    
    def GetName(self):
        return self.__element.GetName()
    
    def GetType(self):
        type = self.__element.GetType()
        if isinstance(type, CElementAlias):
            return ElementAlias.IElementAlias(type)
        elif isinstance(type, CElementType):
            return ElementType.IElementType(type)
    
    def GetDiagrams(self):
        node = self.__element.GetNode()
        if node is not None:
            for diagram in node.GetDiagrams():
                yield Diagram.IDiagram(self.__plugin, diagram)
    
    def GetConnections(self):
        for connection in self.__element.GetConnections():
            yield ConnectionObject.IConnectionObject(self.__plugin, connection)
        
    def GetChildren(self):
        node = self.__element.GetNode()
        if node is not None:
            for child in node.GetChilds():
                yield IElementObject(self.__plugin, child.GetObject())
        
    def GetAppears(self):
        for diagram in self.__element.GetAppears():
            yield Diagram.IDiagram(self.__plugin, diagram)
    
    @params(object, object)
    def ConnectWith(self, other, connectionType):
        cmd = CCreateConnectionObjectCommand(self.__element, other._element, connectionType._connectionType)
        self.__plugin.GetTransaction().Execute(cmd)
        return ConnectionObject.IConnectionObject(self.__plugin, cmd.GetConnectionObject())
    
    @params(object)
    def CreateDiagram(self, diagramType):
        cmd = CCreateDiagramCommand(diagramType._diagramType, self.__element.GetNode())
        self.__plugin.GetTransaction().Execute(cmd)
        return Diagram.IDiagram(self.__plugin, cmd.GetDiagram())
    
    @params(object)
    def CreateChildElement(self, elementType):
        cmd = CCreateElementObjectCommand(elementType._elementType, self.__element.GetNode())
        self.__plugin.GetTransaction().Execute(cmd)
        return IElementObject(self.__plugin, cmd.GetElementObject())
    
    @params(object)
    def ShowIn(self, diagram):
        if diagram.HasElement(self.__element):
            raise PluginInvalidMethodParameters(self.__element.GetUID(), "element is already shown on given diagram")
        
        cmd = CShowElementCommand(self.__element, diagram._diagram)
        self.__plugin.GetTransaction().Execute(cmd)
        return ElementVisual.IElementVisual(self.__plugin, cmd.GetElementVisual())
