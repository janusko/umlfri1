from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder
from lib.Domains.Modifications import CReplaceAttributeModification
from lib.Domains.Modifications.DeleteAttributeModification import CDeleteAttributeModification


class CElementModificationBuilder:

    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()

    def __init__(self, projectNode):
        self.projectNode = projectNode
        self.elementTypeModifications = {}

    def AddDomainAttribute(self, elementType, domain, attributeID, attributeProperties):
        self.ReplaceDomainAttribute(elementType, domain, attributeID, attributeProperties)

    def ReplaceDomainAttribute(self, elementType, domain, attributeID, attributeProperties):
        self.__AppendDomainAttributeModification(elementType, domain,
                                                 CReplaceAttributeModification(attributeID, attributeProperties))

    def DeleteDomainAttribute(self, elementType, domain, attributeID):
        self.__AppendDomainAttributeModification(elementType, domain,
                                                 CDeleteAttributeModification(attributeID))

    def GetElementTypeModifications(self):
        return self.elementTypeModifications

    def BuildMetamodel(self):
        return self.__modifiedMetamodelBuilder.BuildMetamodel(self.projectNode, self.elementTypeModifications)

    def __AppendDomainAttributeModification(self, elementType, domain, modification):
        modifications = self.__GetElementTypeModifications(elementType)
        list = modifications.setdefault(domain, [])
        list.append(modification)

    def __GetElementTypeModifications(self, elementType):
        return self.elementTypeModifications.setdefault(elementType, {})
