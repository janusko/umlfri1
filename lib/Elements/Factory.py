import os
import os.path
import weakref

from lib.Exceptions.DevException import *
from Type import CElementType
from Alias import CElementAlias
from lib.Distconfig import SCHEMA_PATH
from lib.consts import METAMODEL_NAMESPACE
from lib.Drawing.Objects import ALL
from lib.Drawing.Context import BuildParam
from lib.Depend.libxml import etree
from lib.Base import CBaseObject

xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "metamodel.xsd"))
xmlschema = etree.XMLSchema(xmlschema_doc)


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
