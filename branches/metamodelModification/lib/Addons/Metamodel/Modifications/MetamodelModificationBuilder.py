from lib.Addons.Metamodel.Modifications.ElementModificationBuilder import CElementModificationBuilder
from lib.Addons.Metamodel.Modifications.MetamodelModification import CMetamodelModification
from lib.Addons.Metamodel.Modifications.ModificationTreeBuilder import CModificationTreeBuilder


class CMetamodelModificationBuilder:

    def __init__(self, metamodel, projectNode):
        self.elementModifications = {}
        self.metamodel = metamodel
        self.projectNode = projectNode

    def CreateElementModifications(self, elementNode):
        return self.__GetElementModifications(elementNode)

    def Build(self):
        objectTypeMapping = CModificationTreeBuilder(self.metamodel, self.projectNode,
                                                     self.elementModifications).BuildTree()

        return CMetamodelModification(objectTypeMapping)

    def __GetElementModifications(self, elementNode):
        return self.elementModifications.setdefault(elementNode, CElementModificationBuilder(elementNode))

