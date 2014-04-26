from .Decorators import params, mainthread, polymorphic

from . import ConnectionType
from . import DiagramType
from . import DomainType
from . import ElementType

from lib.Exceptions import ParamValueError


class IMetamodel(object):
    def __init__(self, metamodel):
        self.__metamodel = metamodel
    
    @property
    def uid(self):
        return self.__metamodel.GetUID()
    
    def GetUri(self):
        return self.__metamodel.GetUri()
    
    def GetVersion(self):
        return self.__metamodel.GetVersionString()
    
    @params(str)
    def GetDiagram(self, name):
        return DiagramType.IDiagramType(self.__metamodel.GetDiagramFactory().GetDiagram(name))
        
    def GetDiagrams(self):
        for diagram in self.__metamodel.GetDiagramFactory():
            yield DiagramType.IDiagramType(diagram)
    
    @params(str)
    def GetElement(self, name):
        return ElementType.IElementType(self.__metamodel.GetElementFactory().GetElement(name))
    
    def GetElements(self):
        for element in self.__metamodel.GetElementFactory().IterTypes():
            yield ElementType.IElementType(element)
    
    @params(str)
    def GetConnection(self, name):
        return ConnectionType.IConnectionType(self.__metamodel.GetConnectionFactory().GetConnection(name))
    
    def GetConnections(self):
        for connection in self.__metamodel.GetConnectionFactory().IterTypes():
            yield  ConnectionType.IConnectionType(connection)
    
    def GetDomains(self):
        for domain in self.__metamodel.GetDomainFactory().IterTypes():
            yield DomainType.IDomainType(domain)
    
    @params(str)
    def ListDir(self, path):
        try:
            return self.__metamodel.GetStorage().listdir(path)
        except:
            raise ParamValueError('invalid path')
    
    @params(str)
    def ReadFile(self, path):
        try:
            return self.__metamodel.GetStorage().read_file(path)
        except:
            raise ParamValueError('invalid path')
