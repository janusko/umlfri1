from lib.Domains.ModifiedFactory import CModifiedDomainFactory
from lib.Domains.ModifiedType import CModifiedDomainType
from lib.Elements import CElementObject
from lib.Elements.ModifiedType import CModifiedElementType

class CModificationTreeBuilder:

    def __init__(self, projectRoot, elementModifications):
        self.projectRoot = projectRoot
        self.elementModifications = elementModifications

    def BuildTree(self):

        # TODO: create element types from top to bottom of the project tree

        # TODO: create modifications only for specified element types (i.e. when applied to package, with modifications
        # to class attributes, don't create modified type for package element)

        elementTypes = {}

        elementTypeMappings = {}

        # OUT of DATE:
        # assuming that iterating element modifications dictionary is from the project node with lowest depth to highest

        # now using project root to start the tree building process

        nodesToProcess = [(self.projectRoot, {})]
        while len(nodesToProcess) > 0:
            elementNode, elementTypes = nodesToProcess.pop(0)
            element = elementNode.GetObject()
            if element is CElementObject:
                if elementNode in self.elementModifications:
                    modifications = self.elementModifications[elementNode]
                    modifiedElementType = self.__BuildTypeFromNode(elementTypes, elementNode, modifications)
                    elementTypes = elementTypes[:]
                    elementTypes[modifiedElementType.GetId()] = modifiedElementType

                    elementTypeMappings[element] = modifiedElementType
                else:
                    elementType = element.GetType()
                    if elementType.GetId() in elementTypes:
                        elementTypeMappings[element] =  elementTypes[elementType.GetId()]

            children = tuple((c, elementTypes) for c in elementNode.GetChilds())
            nodesToProcess.extend(children)

        return elementTypeMappings

    #     while len(self.elementModifications) > 0:
    #         elementNode, modifications = self.elementModifications.popitem()
    #         modifiedElementType = self.__BuildTypeFromNode(elementTypes, elementNode, modifications)
    #
    #         # store in nodesToProcess item also elementTypes, create new when building type from node
    #         nodesToProcess.extend(self.__GetChildElements(elementNode))
    #
    #         while len(nodesToProcess) > 0:
    #             elementNode = nodesToProcess.pop(0)
    #
    #             # stop traversing tree, if we find project node, that has modifications
    #             if elementNode in self.elementModifications:
    #                 break
    #
    #             # only creating mapping if the type name matches
    #             element = elementNode.GetObject()
    #             if element.GetType().GetName() == modifiedElementType.GetName():
    #                 objectTypeMappings[element] = modifiedElementType
    #
    #             nodesToProcess.extend()
    #
    # def __GetChildElements(self, node):
    #     for c in node.GetChilds():
    #         if c.GetObject() is CElementObject:
    #             yield c


    def __BuildTypeFromNode(self, elementTypes, elementNode, elementModifications):
        modifications = elementModifications[elementNode]
        element = elementNode.GetObject()
        elementType = element.GetType()

        if elementTypes.has_key(elementType.GetName()):
            elementType = elementTypes[elementType.GetName()]

        factory = CModifiedDomainFactory(elementType.GetFactory())
        self.__CreateModifiedDomainTypes(factory, element, modifications)
        modifiedElementType = CModifiedElementType(elementType)
        modifiedElementType.SetDomain(factory.GetDomain(elementType.GetDomain().GetName()))
        return modifiedElementType


    def __CreateElementTypeAssignments(self, elementNode, elementType):
            nodes = [elementNode]
            while len(nodes) > 0:
                elementNode = nodes.pop()

                # yield elementNode.GetObject(),
                # elementTypes[element] = modifiedElementType

    def __CreateModifiedDomainTypes(self, factory, element, domainModifications):
        for name, modifications in domainModifications:
            domain = CModifiedDomainType(element.GetType(), factory, modifications)
            factory.AddDomain(domain)