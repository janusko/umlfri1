import weakref
from Type import CElementType


class CModifiedElementType(CElementType):

    def __init__(self, parentType, factory):
        CElementType.__init__(self, None, parentType.GetId())
        self.parentType = weakref.ref(parentType)
        self.factory = lambda: factory
