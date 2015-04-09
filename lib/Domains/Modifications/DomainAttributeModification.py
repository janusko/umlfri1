from lib.Base import CBaseObject


class DomainAttributeModificationType():
    REPLACE = 1
    DELETE = 2

class CDomainAttributeModification(CBaseObject):

    def __init__(self, attributeID):
        self.attributeID = attributeID

    def GetType(self):
        return self.type

    def GetAttributeID(self):
        return self.attributeID

    def ApplyToAttributes(self, attributes):
        pass