from lib.Base import CBaseObject


class CDomainAttributeModification(CBaseObject):

    def __init__(self, attributeID, type):
        self.attributeID = attributeID
        self.type =  type

    def ApplyToAttributes(self, attributes):
        return attributes