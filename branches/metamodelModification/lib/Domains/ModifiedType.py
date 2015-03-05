import weakref
from Type import CDomainType


class CModifiedDomainType(CDomainType):

    def __init__(self, parentType, modifications):
        CDomainType.__init__(parentType.GetName(), parentType.GetFactory())
        self.parentType = weakref.ref(parentType)
        self.modifications = modifications

    def AppendAttribute(self, id, name, type = None, default = None, hidden=False):
        CDomainType.AppendAttribute(id, name, type, default, hidden)

    def HasAttribute(self, id):
        return CDomainType.HasAttribute(self)

    def GetAttribute(self, id):
        return CDomainType.GetAttribute(id)

    def IterAttributeIDs(self):
        return CDomainType.IterAttributeIDs(self)
