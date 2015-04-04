from lib.Addons.Metamodel.Modifications.ElementObjectTypeMapping import CElementObjectTypeMapping
from lib.Addons.Metamodel.ModifiedMetamodel import CModifiedMetamodel
from lib.Domains.ModifiedFactory import CModifiedDomainFactory
from lib.Domains.ModifiedType import CModifiedDomainType
from lib.Elements import CElementObject, CElementFactory, CElementAlias
from lib.Elements.ModifiedType import CModifiedElementType
from lib.Exceptions.DevException import MetamodelModificationError


class CModificationTreeBuilder:

    def __init__(self, projectNode, elementModifications):
        self.projectNode = projectNode
        self.elementModifications = elementModifications

    def BuildTree(self):
        factory = self.projectNode.GetMetamodel().GetElementFactory()
        for name in self.elementModifications.iterkeys():
            if not factory.HasType(name):
                raise MetamodelModificationError('Creating new element types is not currently supported.')

            type = factory.GetElement(name)

            if isinstance(type, CElementAlias):
                raise MetamodelModificationError('Cannot modify element alias "{0}"'.format(type))

        # start with original element types from original metamodel
        # element aliases are skipped, since they are not supported
        elementTypes = {type.GetId(): type
                        for type in factory.IterTypes()
                        if not isinstance(type, CElementAlias)}

        elementTypeMappings = {}

        # algorithm overview:
        #  - traverse project tree and create mappings between element object and its type
        #  - when given project node has modifications, stop and process modifications
        #     - create modified element type for all modifications that this project node has defined
        #     - for this project and its descendants, mappings will be created with this modified types


        nodesToProcess = [(self.projectNode, elementTypes)]
        while len(nodesToProcess) > 0:
            elementNode, elementTypes = nodesToProcess.pop(0)
            element = elementNode.GetObject()
            if isinstance(element, CElementObject):
                if elementNode == self.projectNode:
                    modifiedElementType = self.__BuildTypeFromNode(elementTypes, elementNode, self.elementModifications)
                    elementTypes = dict(elementTypes)

                    elementTypeMappings[element] = CElementObjectTypeMapping(element, modifiedElementType)
                else:
                    elementType = element.GetType()
                    elementTypeMappings[element] = CElementObjectTypeMapping(element, elementTypes[elementType.GetId()])

            children = tuple((c, elementTypes) for c in self.__GetChildElements(elementNode))
            nodesToProcess.extend(children)

        return elementTypeMappings

    @staticmethod
    def __GetChildElements(node):
        for c in node.GetChilds():
            if isinstance(c.GetObject(), CElementObject):
                yield c

    def __BuildTypeFromNode(self, elementTypes, elementNode, elementTypeModifications):
        factory = self.__BuildFactoryFromNode(elementTypes, elementNode, elementTypeModifications)

        return factory.GetElement(elementNode.GetObject().GetType().GetId())

    def __BuildFactoryFromNode(self, elementTypes, elementNode, elementTypeModifications):
        modifiedMetamodel = CModifiedMetamodel(elementNode.GetObject().GetType().GetMetamodel(), elementTypeModifications)

        modifiedElementFactory = modifiedMetamodel.GetElementFactory()

        # similar algorithm as above for creating element object <-> type mappings
        # - encapsulate types from elementTypes with new element factory
        # - if there are modifications for given element type, stop and process them:
        #   - create modified domain factory
        #   - create modified domain types
        # - replace types in elementTypes with the new, modified types

        for id in elementTypes.keys():
            elementType = elementTypes[id]

            modifiedElementType = CModifiedElementType(elementType, modifiedElementFactory)
            modifiedElementFactory.AddType(modifiedElementType)

            domainfactory = elementType.GetDomain().GetFactory()
            if elementTypeModifications.has_key(id):
                modifications = elementTypeModifications[id]

                domainfactory = CModifiedDomainFactory(elementType.GetDomain().GetFactory())
                self.__CreateModifiedDomainTypes(domainfactory, modifications)

            modifiedElementType.SetDomain(domainfactory.GetDomain(elementType.GetDomain().GetName()))

            elementTypes[id] = modifiedElementType

        return modifiedElementFactory

    def __CreateModifiedDomainTypes(self, factory, domainModifications):
        for name, modifications in domainModifications.iteritems():
            domain = CModifiedDomainType(factory.GetDomain(name), factory, modifications)
            factory.AddDomain(domain)