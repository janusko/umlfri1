import os
import os.path
from lib.Exceptions.DevException import *
from Type import CDomainType
from lib.config import config
from lib.consts import METAMODEL_NAMESPACE
from lib.Drawing.Objects import ALL
from Parser import CDomainParser
from lib.Exceptions import DomainFactoryError
from lib.Depend.etree import etree, HAVE_LXML

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
        
        self.domains = {}
        self.path = path
        
        self.storage = storage
        for file in storage.listdir(self.path):
            if file.endswith('.xml'):
                self.__Load(os.path.join(self.path, file))
        
        for domain in self.domains.itervalues():
            result = domain.EmptyTypes()
            if result:
                raise DomainFactoryError(
                    'Domain "%s" has attribute%s without type: %s '%(
                    domain.GetName(), ('s' if len(result) > 1 else ''),
                    ', '.join([('"%s"'%item) for item in result])))
            
            result = domain.UndefinedImports()
            if result:
                raise DomainFactoryError(
                    'Domain "%s" imports unknown domain%s: %s '%(
                    domain.GetName(), ('s' if len(result) > 1 else ''),
                    ', '.join([('"%s"'%item) for item in result])))
            
            loop = domain.HasImportLoop()
            if loop:
                raise DomainFactoryError('Import loop detected: ' + loop)
            
            domain.CheckMissingInfo()
    
    def GetDomain(self, id):
        """
        @return: Domain type by name
        @rtype: L{CDomainType<Type.CDomainType>}
        
        @param id: Element type name
        @type  id: string
        """
        if not id in self.domains:
            raise DomainFactoryError('unrecognized domain name ' + id)
        
        return self.domains[id]
    
    def HasDomain(self, id):
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
        
        if HAVE_LXML:
            if not xmlschema.validate(root):
                raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        if root.tag == METAMODEL_NAMESPACE + 'Domain':
            self.__LoadDomain(root)
        
    def __LoadDomain(self, root, name=None):
        '''
        Load Domain from root node
        
        @param root: node <Domain>
        
        @param name: name of parent domain, None for root domain
        @type name: str  
        '''
        if name is None:
            name = root.get('id')
            if name is None:
                raise DomainFactoryError('Undefined root domain id')
            if name.find('.') != -1:
                raise DomainFactoryError('"." not allowed in domain id')
            if name in self.domains:
                raise DomainFactoryError('Duplicate domain identifier')
        elif root.get('id') is not None:
            raise DomainFactoryError('Domain id not allowed in nested domain')
        
        obj = CDomainType(name, self)
        self.domains[name] = obj
        
        for node in root:
            if node.tag == METAMODEL_NAMESPACE + 'Import':
                obj.AppendImport(node.get('id'))
            
            elif node.tag == METAMODEL_NAMESPACE + 'Attribute': 
                self.__LoadAttribute(obj, node)
            
            elif node.tag == METAMODEL_NAMESPACE + 'Parse':
                obj.AppendParser(CDomainParser(**dict(node.items())))
            
            
            else:
                raise DomainFactoryError('Unknown Section: %s'%(section.tag, ))
            
        
    
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
                obj.SetList(id, **self.__LoadList(option))
            
            elif option.tag == METAMODEL_NAMESPACE + 'Domain':
                name = obj.GetName() +'.' + id
                self.__LoadDomain(option, name)
                obj.AppendImport(name)
                if obj.GetAttribute(id)['type'] is None:
                    obj.GetAttribute(id)['type'] = name
                elif obj.GetAttribute(id)['type'] == 'list':
                    obj.SetList(id, type = name)
                else:
                    raise DomainFactoryError('Nested Domain is not allowed '
                        'in attribute of type ' + obj.GetAttribute(id)['type'])
    
    def __LoadList(self, node):
        '''
        Parse <List> node of attribute
        
        @return: all the information for the list that can be read from node
        @rtype: dict
        
        @param node: <List> XML node
        @type: xml node
        '''
        
        result = dict(node.items())
        for option in node:
            if option.tag == METAMODEL_NAMESPACE + 'Parse':
                result['parser'] = CDomainParser(**dict(option.items()))
        
        return result
