from lib.Base import CBaseObject


class CDomainAttributeModification(CBaseObject):

    def __init__(self, attributeID):
        self.attributeID = attributeID

    def GetAttributeID(self):
        return self.attributeID

    def ApplyToAttributes(self, attributes):
        pass