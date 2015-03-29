import weakref

from lib.Exceptions.DevException import *
from lib.Base import CBaseObject


class CElementFactory(CBaseObject):
    """
    Factory, that creates element type objects
    """
    def __init__(self, metamodel, types = None):
        """
        Create the element factory

        @param metamodel: Parent metamodel.
        @type metamodel: L{CMetamodel<lib.Addons.Metamodel.Metamodel.CMetamodel>}
        @param types: Initial element types.
        @type types: dict of string and CElementType
        """
        self.metamodel = weakref.ref(metamodel)
        self.types = types or {}

    def AddTypes(self, types):
        for type in types:
            self.AddType(type)

    def AddType(self, type):
        if type.GetFactory() != self:
            raise FactoryError('type "%s" has invalid factory', type.GetId())

        self.types[type.GetId()] = type

    def GetElement(self, type):
        """
        Get element type by name
        
        @param type: Element type name
        @type  type: string
        """
        if not type in self.types:
            raise FactoryError('unrecognized elementType name "%s"' % type)
        return self.types[type]
    
    def IterTypes(self):
        '''
        iterator over element types
        
        @rtype: L{CElementType<CElementType>}
        '''
        for type in self.types.itervalues():
            yield type
    
    def HasType(self, id):
        return id in self.types

    def GetMetamodel(self):
        return self.metamodel()

