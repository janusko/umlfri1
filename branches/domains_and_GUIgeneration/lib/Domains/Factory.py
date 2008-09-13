import os
import os.path
from lib.Exceptions.DevException import *
from Type import CDomainType
from lib.config import config
from lib.consts import METAMODEL_NAMESPACE
from lib.Drawing.Objects import ALL

#try to import necessary lybraries for XML parsing
try:
    from lxml import etree
    HAVE_LXML = True
except ImportError:
    HAVE_LXML = False
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
            except ImportError:
                # normal ElementTree install
                import elementtree.ElementTree as etree
               
#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(config['/Paths/Schema'], "metamodel.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)


class EDomainFactory(Exception): pass

class CDomainFactory(object):
    '''
    Factory to create Domains
    '''
    
    def __init__(self, storage, path):
        """
        Create the domain factory
        
        @param storage: Storage in which is file located
        @type  storage: L{CAbstractStorage<lib.Storages.AbstractStorage.CAbstractStorage>}
        
        @param path: Path to directory with connection metamodel XMLs
        @type path: string
        """
        
        self.domains = {}
        self.path = path
        
        self.storage = storage
        for file in storage.listdir(self.path):
            if file.endswith('.xml'):
                print file
                self.__Load(os.path.join(self.path, file))
        
        for domain in self.domains.itervalues():
            result = domain.UndefinedImports()
            if result:
                raise EDomainFactory(
                    'Domain "%s" imports unknown domain%s: %s '%(
                    domain.GetName(), ('s' if len(result) > 1 else ''),
                    ', '.join([('"%s"'%item) for item in result])))
            
            loop = domain.HasImportLoop()
            if loop:
                raise EDomainFactory('Import loop detected: ' + loop)
            
            domain.CheckMissingInfo()
    
    def GetDomain(self, id):
        """
        @return: Domain type by name
        @rtype: L{CDomainType<Type.CDomainType>}
        
        @param id: Element type name
        @type  id: string
        """
        if not id in self.domains:
            raise EDomainFactory('unrecognized identifier')
        
        return self.domains[id]
    
    def RecognizedDomain(self, id):
        '''
        @return: True if domain identifier is registered in current factory
        @rtype: bool
        
        @param id: Element type name
        @type  id: string
        '''
        return id in self.domains
    
    def __Load(self, path):
        '''
        Load XML from given path
        
        @param path: path to the XML file
        @type path: str
        '''
        
        root = etree.XML(self.storage.read_file(path))
        
        #~ if HAVE_LXML:
            #~ if not xmlschema.validate(root):
                #~ raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        if root.tag == METAMODEL_NAMESPACE + 'Domain':
            self.__LoadDomain(root)
        
    def __LoadDomain(self, root):
        '''
        Load Domain from root node
        
        @param root: node <Domain>
        '''
        if root.get('id') in self.domains:
            raise EDomainFactory('Duplicate domain identifier')
        
        obj = CDomainType(root.get('id'), self)
        
        for node in root:
            if node.tag == METAMODEL_NAMESPACE + 'Import':
                obj.AppendImport(node.get('id'))
            
            elif node.tag == METAMODEL_NAMESPACE + 'Attribute': 
                self.__LoadAttribute(obj, node)
            
            elif node.tag == METAMODEL_NAMESPACE + 'Parse':
                obj.AppendParser(**dict(node.items()))
            
            elif node.tag == METAMODEL_NAMESPACE + 'Domain':
                self.__LoadDomain(node)
                obj.AppendImport(node.get('id'))
            
            else:
                raise EDomainFactory('Unknown Section: %s'%(section.tag, ))
            
        self.domains[root.get('id')] = obj
    
    def __LoadAttribute(self, obj, attribute):
        '''
        Load <Attribute> node of Domain
        
        @param obj: domain type to be altered
        @type obj: L{CDomainType<Type.CDomainType>}
        
        @param attribute: xml node
        '''
        
        obj.AppendAttribute(**dict(attribute.items()))
        id = attribute.get('id')
        for option in attribute:
            if option.tag == METAMODEL_NAMESPACE + 'Enum':
                obj.AppendEnumValue(id, option.text)

            elif option.tag == METAMODEL_NAMESPACE + 'List':
                obj.SetList(id, **dict(option.items()))
            
            elif node.tag == METAMODEL_NAMESPACE + 'Domain':
                self.__LoadDomain(node)
                obj.AppendImport(node.get('id'))
