from lib.Addons.Metamodel.Modifications import ModificationTreeBuilder
from lib.Domains.Modifications import CReplaceAttributeModification
from lib.Domains.Modifications.DeleteAttributeModification import CDeleteAttributeModification


class CMetamodelModificationBuilder:
    def __init__(self, projectRoot):
        self.elementModifications = {}
        self.projectRoot = projectRoot

    def AddDomainAttribute(self, elementNode, domain, attributeID, attributeProperties):
        self.ReplaceDomainAttribute(elementNode, domain, attributeID, attributeProperties)

    def ReplaceDomainAttribute(self, elementNode, domain, attributeID, attributeProperties):
        self.__AppendDomainAttributeModification(elementNode, domain,
                                                 CReplaceAttributeModification(attributeID, attributeProperties))

    def DeleteDomainAttribute(self, elementNode, domain, attributeID):
        self.__AppendDomainAttributeModification(elementNode, domain,
                                                 CDeleteAttributeModification(attributeID))

    def Build(self):
        objectTypeMapping = ModificationTreeBuilder(self.projectRoot, self.elementModifications).BuildTree()

    def __AppendDomainAttributeModification(self, elementNode, domain, modification):
        modifications = self.__GetElementModifications(elementNode)
        list = modifications.setdefault(domain, [])
        list.append(modification)

    def __GetElementModifications(self, elementNode):
        return self.elementModifications.setdefault(elementNode, {})
