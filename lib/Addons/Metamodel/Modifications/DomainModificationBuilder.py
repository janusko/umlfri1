from lib.Domains.Modifications import CReplaceAttributeModification
from lib.Domains.Modifications.DeleteAttributeModification import CDeleteAttributeModification


class CDomainModificationBuilder:

    def __init__(self):
        self.domainModifications = {}

    def AddDomainAttribute(self, domain, attributeID, attributeProperties):
        self.ReplaceDomainAttribute(domain, attributeID, attributeProperties)

    def ReplaceDomainAttribute(self, domain, attributeID, attributeProperties):
        self.__AppendDomainAttributeModification(domain,
                                                 CReplaceAttributeModification(attributeID, attributeProperties))

    def DeleteDomainAttribute(self, domain, attributeID):
        self.__AppendDomainAttributeModification(domain,
                                                 CDeleteAttributeModification(attributeID))

    def GetDomainModifications(self):
        return self.domainModifications

    def __AppendDomainAttributeModification(self, domain, modification):
        list = self.domainModifications.setdefault(domain, [])
        list.append(modification)