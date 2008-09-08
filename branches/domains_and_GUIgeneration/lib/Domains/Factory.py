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
        
        self.types = {}
        self.path = path
        
        self.storage = storage
        for file in storage.listdir(self.path):
            if file.endswith('.xml'):
                self.__Load(os.path.join(self.path, file))
    
    def GetDomain(self, name):
        """
        @return: Domain type by name
        @rtype: L{CDomainType<Type.CDomainType>}
        
        @param type: Element type name
        @type  type: string
        """
        return self.types[type]
    
    def __Load(self, path):
        '''
        Load XML from given path
        
        @param path: path to the XML file
        @type path: str
        '''
        
        root = etree.XML(self.storage.read_file(file_path))
        
        if HAVE_LXML:
            if not xmlschema.validate(root):
                raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        obj = CDomainPath(root.get('id'))
        
        for section in root:
            {   METAMODEL_NAMESPACE + 'Import': self.__LoadImport
                METAMODEL_NAMESPACE + 'Attributes': self.__LoadAttributes
            }[section.tag()](obj, section)
            
        self.types[root.get('id')] = obj
    
    def __LoadImport(self, obj, section):
        '''
        Load <Import> part of Domain
        
        Import part is used for easier detection of loops in use of domains
        
        @param obj: domain type to be altered
        @type obj: L{CDomainType<Type.CDomainType>}
        
        @param section: xml node <Import>...</Import>
        @type section:
        '''
        
        for domain in section:
            obj.AppendImport(domain.get('value'))
    
    def __LoadAttributes(self, obj, section):
        '''
        Load <Attributes> section of Domain
        
        Attributes section has information about fields in domain
        
        @param obj: domain type to be altered
        @type obj: L{CDomainType<Type.CDomainType>}
        
        @param section: xml node <Import>...</Import>
        @type section:
        '''
        
        for item in section:
            options = []
            for opt in item:
                options.append(opt.get('value'))
            obj.AppendItem(options = options, **dict(item.items()))
