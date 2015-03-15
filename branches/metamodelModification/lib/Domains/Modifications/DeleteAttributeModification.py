from DomainAttributeModification import CDomainAttributeModification


class CDeleteAttributeModification(CDomainAttributeModification):

    def ApplyToAttributes(self, attributes):
        del attributes[self.attributeID]
