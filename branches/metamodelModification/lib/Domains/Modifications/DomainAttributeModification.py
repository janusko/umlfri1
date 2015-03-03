from lib.Base import CBaseObject


class CDomainAttributeModification(CBaseObject):

    def __init__(self, attributeID, type):
        self.attributeID = attributeID
        self.type =  type

    def ApplyToAttribute(self, attribute):
        name, properties = attribute
        return properties