from lib.Addons.Metamodel.Modifications import CElementModificationBuilder
from lib.Addons.Metamodel.Modifications import CModificationTreeBuilder
from lib.Addons.Metamodel.Modifications.MetamodelModification import CMetamodelModification


class CMetamodelModificationBuilder:

    def __init__(self):
        self.elementModifications = {}

    def CreateElementModifications(self, elementNode):
        return self.__GetElementModifications(elementNode)

    def Build(self):
        objectTypeMapping = CModificationTreeBuilder(self.elementNode, self.elementModifications).BuildTree()

        return CMetamodelModification(objectTypeMapping)

    def __GetElementModifications(self, elementNode):
        return self.elementModifications.setdefault(elementNode, CElementModificationBuilder(elementNode))

