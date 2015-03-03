from DomainAttributeModification import CDomainAttributeModification


class CReplaceAttributeModification(CDomainAttributeModification):

    def __init__(self, attributeID, attributeProperties):
        super.__init__(attributeID)
        self.attributeProperties = attributeProperties

    def ApplyToAttribute(self, attribute):
        return self.attributeProperties