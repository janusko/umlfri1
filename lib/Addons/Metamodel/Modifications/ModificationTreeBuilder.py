from lib.Domains.ModifiedFactory import CModifiedDomainFactory
from lib.Domains.ModifiedType import CModifiedDomainType
from lib.Elements import CElementObject
from lib.Elements.ModifiedFactory import CModifiedElementFactory
from lib.Elements.ModifiedType import CModifiedElementType
from lib.Exceptions.DevException import MetamodelModification, MetamodelModificationError


class CModificationTreeBuilder:

    def __init__(self, metamodel, projectRoot, elementModifications):
        self.metamodel = metamodel
        self.projectRoot = projectRoot
        self.elementModifications = elementModifications

    def BuildTree(self):

        # start with original element types from original metamodel
        elementTypes = {id: self.metamodel.GetElementFactory().GetElement(id)
                        for id in self.metamodel.GetElementFactory().IterTypes()}

        elementTypeMappings = {}

        # algorithm overview:
        #  - traverse project tree and create mappings between element object and its type
        #  - when given project node has modifications, stop and process modifications
        #     - create modified element type for all modifications that this project node has defined
        #     - for this project and its descendants, mappings will be created with this modified types


        nodesToProcess = [(self.projectRoot, elementTypes)]
        while len(nodesToProcess) > 0:
            elementNode, elementTypes = nodesToProcess.pop(0)
            element = elementNode.GetObject()
            if element is CElementObject:
                if elementNode in self.elementModifications:
                    modifications = self.elementModifications[elementNode].GetElementTypeModifications()
                    modifiedElementType = self.__BuildTypeFromNode(elementTypes, elementNode, modifications)
                    elementTypes = elementTypes[:]
                    elementTypes[modifiedElementType.GetId()] = modifiedElementType

                    elementTypeMappings[element] = modifiedElementType
                else:
                    elementType = element.GetType()
                    if elementType.GetId() in elementTypes:
                        elementTypeMappings[element] = elementTypes[elementType.GetId()]

            children = tuple((c, elementTypes) for c in self.__GetChildElements(elementNode))
            nodesToProcess.extend(children)

        return elementTypeMappings

    @staticmethod
    def __GetChildElements(node):
        for c in node.GetChilds():
            if c.GetObject() is CElementObject:
                yield c


    def __BuildTypeFromNode(self, elementTypes, elementNode, elementTypeModifications):
        factory = self.__BuildTypeFromNode(elementTypes, elementNode, elementTypeModifications)

        return factory.GetElement(elementNode.GetObject().GetType().GetId())

    def __BuildFactoryFromNode(self, elementTypes, elementNode, elementTypeModifications):
        modifiedElementFactory = CModifiedElementFactory(elementNode.GetObject().GetFactory())

        for type, modifications in elementTypeModifications.iteritems():
            if not elementTypes.has_key(type):
                raise MetamodelModificationError('Creating new element types is not currently supported.')

            elementType = elementTypes[type]

            factory = CModifiedDomainFactory(elementType.GetDomain().GetFactory())
            self.__CreateModifiedDomainTypes(factory, elementType, modifications)
            modifiedElementType = CModifiedElementType(elementType, modifiedElementFactory)
            modifiedElementType.SetDomain(factory.GetDomain(elementType.GetDomain().GetName()))
            modifiedElementFactory.AddElement(modifiedElementType)

        return modifiedElementFactory

    def __CreateModifiedDomainTypes(self, factory, domainModifications):
        for name, modifications in domainModifications:
            domain = CModifiedDomainType(factory.GetDomain(name), factory, modifications)
            factory.AddDomain(domain)