from collections import OrderedDict
from lib.Domains import CDomainType
from lib.Domains.Modifications.DomainAttributeModification import DomainAttributeModificationType


class CDomainTypeFactory(object):

    def CreateDomainFromModifications(self, name, factory, attributeModifications):
        attributes = OrderedDict()
        for m in attributeModifications:
            if m.GetType() == DomainAttributeModificationType.REPLACE:
                attributes[m.GetAttributeID()] = m.GetAttributeProperties()

        return CDomainType(name, factory, attributes)