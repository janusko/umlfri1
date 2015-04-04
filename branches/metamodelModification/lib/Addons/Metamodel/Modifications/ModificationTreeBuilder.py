from lib.Addons.Metamodel.Modifications.ElementObjectTypeMapping import CElementObjectTypeMapping
from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder
from lib.Elements import CElementObject, CElementAlias
from lib.Exceptions.DevException import MetamodelModificationError


class CModificationTreeBuilder:

    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()

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

        elementTypeMappings = {}

        # algorithm overview:
        #  - traverse project tree and create mappings between element object and its type
        #  - when given project node has modifications, stop and process modifications
        #     - create modified element type for all modifications that this project node has defined
        #     - for this project and its descendants, mappings will be created with this modified types


        nodesToProcess = [(self.projectNode, self.projectNode.GetMetamodel())]
        while len(nodesToProcess) > 0:
            elementNode, metamodel = nodesToProcess.pop(0)
            element = elementNode.GetObject()
            elementTypeId = elementNode.GetType()
            if isinstance(element, CElementObject):
                if elementNode == self.projectNode:
                    metamodel = self.__modifiedMetamodelBuilder.BuildMetamodel(elementNode, self.elementModifications)

                elementTypeMappings[element] = CElementObjectTypeMapping(element, metamodel.GetElementFactory().GetElement(elementTypeId))

            children = tuple((c, metamodel) for c in self.__GetChildElements(elementNode))
            nodesToProcess.extend(children)

        return elementTypeMappings

    @staticmethod
    def __GetChildElements(node):
        for c in node.GetChilds():
            if isinstance(c.GetObject(), CElementObject):
                yield c

    def __BuildTypeFromNode(self, elementNode, elementTypeModifications):
        factory = self.__modifiedMetamodelBuilder.BuildMetamodel(elementNode, elementTypeModifications)

        return factory.GetElement(elementNode.GetObject().GetType().GetId())
