from lib.Domains import CDomainFactory
from lib.Elements.Factory import CElementFactory
from lib.Diagrams.Factory import CDiagramFactory
from lib.Connections.Factory import CConnectionFactory
from PathFactory import CPathFactory
from lib.Exceptions import MetamodelValidationError
from lib.Elements import CElementType
import os

class CMetamodel(object):
    def __init__(self, storage, uri, version):
        self.__Storage = storage
        self.__PathFactory = CPathFactory(self.__Storage, 'paths.xml')
        self.__DomainFactory = CDomainFactory(self.__Storage, 'domains')
        self.__ElementFactory = CElementFactory(self, self.__Storage, 'elements', self.__DomainFactory)
        self.__DiagramFactory = CDiagramFactory(self.__Storage, 'diagrams')
        self.__ConnectionFactory = CConnectionFactory(self, self.__Storage, 'connections', self.__DomainFactory)
        self.__MetamodelUri = uri
        self.__MetamodelVersion = version
        self.__diagramsList = []
        
        # Metamodel validation
        # Diagram connections are valid
        connectionIds = []
        for connection in self.__ConnectionFactory.types.values():
            connectionIds.append(connection.GetId())
        for diagram in self.__DiagramFactory.types.values():
            for connection in diagram.connections:
                if not connection in connectionIds:
                    raise MetamodelValidationError('Connection "%s" of diagram "%s" is not valid'%(connection,diagram.GetId()))
        
        # Element connections are valid
        for element in self.__ElementFactory.types.values():
            if isinstance(element, CElementType):
                for connection in element.connections:
                    if not connection in connectionIds:
                        raise MetamodelValidationError('Connection "%s" of element "%s" is not valid'%(connection,element.GetId()))
        
        # Diagram elements are valid
        elementIds = []
        for element in self.__ElementFactory.types.values():
            elementIds.append(element.GetId())
        for diagram in self.__DiagramFactory.types.values():
            for element in diagram.elements:
                if not element in elementIds:
                    raise MetamodelValidationError('Element "%s" of diagram "%s" is not valid'%(element,diagram.GetId()))
        
        # Valid diagrams in metamodel
        # not yet implemented
        
    
    def GetStorage(self):
        return self.__Storage
    
    def GetElementFactory(self):
        return self.__ElementFactory
    
    def GetDiagramFactory(self):
        return self.__DiagramFactory
    
    def GetDomainFactory(self):
        return self.__DomainFactory
    
    def GetConnectionFactory(self):
        return self.__ConnectionFactory
    
    def GetPathFactory(self):
        return self.__PathFactory
    
    def GetVersion(self):
        return self.__MetamodelVersion
    
    def GetUri(self):
        return self.__MetamodelUri

    def AddDiagram(self, diagName):
        if (diagName not in self.__diagramsList):
            self.__diagramsList.append(diagName)
        
    def GetDiagrams(self):
        for diag in self.__diagramsList:
            yield diag
