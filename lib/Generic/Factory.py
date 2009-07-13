import os
import os.path
from lib.Exceptions.DevException import *
from lib.config import config
from lib.Depend.etree import etree, HAVE_LXML
import weakref

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(config['/Paths/Schema'], "metamodel.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)


class CGenericFactory(object):
    '''
    Parent class for all Factories
    '''
    
    def __init__(self, storage, metamodel):
        '''
        @param storage: Storage in which metamodel is located
        @type  storage: L{CAbstractStorage<lib.Storages.AbstractStorage.CAbstractStorage>}
        '''
        
        self.storage = storage
        self.__metamodel = weakref.ref(metamodel)
        self.types = {}
        
    @property
    def metamodel(self):
        return self.__metamodel()
    
    def GetType(self, type):
        '''
        @return: GenericType object
        @rtype: L{CGenericType<Type.CGenericType>}
        
        @param type: GenericType name
        @type type: str
        '''
        if not type in self.types:
            raise FactoryError('unrecognized Type name "%s"' % type)
        return self.types[type]
        
    
    def IterTypes(self):
        '''
        iterator over element types
        
        @rtype: L{CGenericType<Type.CGenericType>}
        '''
        for type in self.types.itervalues():
            yield type
    
    
    def _AddType(self, id, type):
        self.types[id] = type
    
    
    __iter__ = IterTypes
        
    
    
