import weakref
from Type import CDomainType
from lib.Domains.Modifications import CReplaceAttributeModification


class CModifiedDomainType(CDomainType):

    def __init__(self, parentType, factory, modifications):
        CDomainType.__init__(parentType.GetName(), factory)
        self.parentType = weakref.ref(parentType)
        self.modifications = modifications

    def AppendAttribute(self, id, name, type = None, default = None, hidden=False):
        properties = {'name': name, 'type': type, 'default': default, 'hidden': (hidden in ('true', '1'))}
        modification = CReplaceAttributeModification(id, properties)
        self.modifications.append(modification)

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
