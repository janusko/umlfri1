from DomainAttributeModification import CDomainAttributeModification


class CDeleteAttributeModification(CDomainAttributeModification):

    def ApplyToAttribute(self, attribute):
        return None