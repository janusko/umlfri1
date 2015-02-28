from .Decorators import params, mainthread, polymorphic

from . import ConnectionType
from . import ElementType
from . import DomainType

class IDiagramType(object):
    def __init__(self, diagramType):
        self.__diagramType = diagramType
    
    @property
    def uid(self):
        return self.__diagramType.GetUID()
    
    @property
    def _diagramType(self):
        return self.__diagramType
    
    def GetName(self):
        return self.__diagramType.GetId()
    
    def GetConnections(self):
        cf = self.__diagramType.GetMetamodel().GetConnectionFactory()
        for connection in self.__diagramType.GetConnections():
            yield ConnectionType.IConnectionType(cf.GetConnection(connection))
    
    def GetElements(self):
        ef = self.__diagramType.GetMetamodel().GetElementFactory()
        for element in self.__diagramType.GetElements():
            yield ElementType.IElementType(ef.GetElement(element))
   
    def GetDomain(self):
        return DomainType.IDomainType(self.__diagramType.GetDomain())
