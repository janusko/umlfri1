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

    def CreateDomain(self, domain):
        self.__GetDomainModifications(domain)

    def GetDomainModifications(self):
        return self.domainModifications

    def __GetDomainModifications(self, domain):
        return self.domainModifications.setdefault(domain, [])

    def __AppendDomainAttributeModification(self, domain, modification):
        list = self.__GetDomainModifications(domain)
        list.append(modification)