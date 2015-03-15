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
        return id in self._GetAttributes()

    def GetAttribute(self, id):
        return self._GetAttributes()[id]

    def IterAttributeIDs(self):
        return CDomainType.IterAttributeIDs(self)

    def _GetAttributes(self):
        attributes = self.parentType()._GetAttributes()[:]
        for m in self.modifications:
            m.ApplyToAttributes(attributes)

        return attributes
