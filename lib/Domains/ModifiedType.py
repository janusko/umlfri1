import weakref
from Type import CDomainType


class CModifiedDomainType(CDomainType):

    def __init__(self, parentType, modifications):
        super.__init__(parentType.GetName(), parentType.GetFactory())
        self.parentType = weakref.ref(parentType)
        self.modifications = modifications
