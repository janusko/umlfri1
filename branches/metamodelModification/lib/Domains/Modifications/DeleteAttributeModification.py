from DomainAttributeModification import CDomainAttributeModification, DomainAttributeModificationType


class CDeleteAttributeModification(CDomainAttributeModification):

    type = DomainAttributeModificationType.DELETE

    def ApplyToAttributes(self, attributes):
        del attributes[self.attributeID]
