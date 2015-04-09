from DomainAttributeModification import CDomainAttributeModification, DomainAttributeModificationType


class CReplaceAttributeModification(CDomainAttributeModification):

    type = DomainAttributeModificationType.REPLACE

    def __init__(self, attributeID, attributeProperties):
        CDomainAttributeModification.__init__(self, attributeID)
        self.attributeProperties = attributeProperties

    def ApplyToAttributes(self, attributes):
        attributes[self.attributeID] = self.attributeProperties