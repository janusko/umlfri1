from DomainAttributeModification import CDomainAttributeModification


class CReplaceAttributeModification(CDomainAttributeModification):

    def __init__(self, attributeID, attributeProperties):
        CDomainAttributeModification.__init__(self, attributeID)
        self.attributeProperties = attributeProperties

    def ApplyToAttributes(self, attributes):
        attributes[self.attributeID] = self.attributeProperties