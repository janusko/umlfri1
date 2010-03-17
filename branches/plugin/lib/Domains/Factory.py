import os
import os.path
import re
from lib.Exceptions.DevException import *
from Type import CDomainType
from lib.Distconfig import SCHEMA_PATH
from lib.consts import METAMODEL_NAMESPACE
from Parser import CDomainParser
from Joiner import CDomainJoiner
from lib.Exceptions import DomainFactoryError
from lib.Depend.etree import etree, HAVE_LXML
from lib.Base import CBaseObject

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "metamodel.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)


class CDomainFactory(CBaseObject):
    '''
    Factory to create Domains
    
    @ivar domains: dictionary with domain names as keys and domain types as values
    '''
    IDENTIFIER = re.compile('[a-zA-Z][a-zA-Z0-9_]*')
    startPageDomain = CDomainType('@StartPage', None)
    startPageDomain.AppendAttribute('name', 'Name', 'str')
    
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
                    'Domain "%s" has attribute "%s" without type: "%s" '%(
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
            domain.CheckDefault()
            
    def GetDomain(self, id):
        """
        @return: Domain type by name
        @rtype: L{CDomainType<Type.CDomainType>}
        
        @param id: Element type name
        @type  id: string
        """
        if id is None:
            return self.startPageDomain
            
        if not id in self.domains:
            raise DomainFactoryError('unrecognized domain name "%s"' % id)
        
        return self.domains[id]
    
    def IterTypes(self):
        '''
        iterator over domain types
        
        @rtype: L{CDomainType<CDomainType>}
        '''
        for type in self.domains.itervalues():
            yield type
            
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
            if self.IDENTIFIER.match(name) is None:
                raise DomainFactoryError('Name "%s" is not valid' %name)
            if name in self.domains:
                raise DomainFactoryError('Duplicate domain identifier "%s"' % name)
        elif root.get('id') is not None:
            raise DomainFactoryError('Domain id not allowed in nested domain "%s"' % name)
        
        obj = CDomainType(name, self)
        self.domains[name] = obj
        
        for node in root:
            if node.tag == METAMODEL_NAMESPACE + 'Import':
                if '.' in node.get('id'):
                    raise DomainFactoryError('Explicit import of local domain not allowed in "%s"' % name)
                obj.AppendImport(node.get('id'))
            
            elif node.tag == METAMODEL_NAMESPACE + 'Attribute': 
                self.__LoadAttribute(obj, node)
            
            elif node.tag == METAMODEL_NAMESPACE + 'Parse':
                obj.AppendParser(CDomainParser(**dict(node.items())))
            elif node.tag == METAMODEL_NAMESPACE + 'Join':
                obj.AppendJoiner(CDomainJoiner(**dict(node.items())))                
                
            else:
                raise DomainFactoryError('Unknown Section "%s" in domain "%s"'%(name, section.tag, ))
            
        
    
    def __LoadAttribute(self, obj, attribute):
        '''
        Load <Attribute> node of Domain
        
        @param obj: domain type to be altered
        @type obj: L{CDomainType<Type.CDomainType>}
        
        @param attribute: xml node
        '''
        id = attribute.get('id')
        if self.IDENTIFIER.match(id) is None:
            raise DomainFactoryError('Name "%s" is not valid' %id)
        type = attribute.get('type')
        default = attribute.get('default')
        if type is not None and '.' in type:
            raise DomainFactoryError('Local domain "%s" cannot be used as explicitly '
                'set type of "%s.%s"' % (type, obj.GetName(), id))
        obj.AppendAttribute(**dict(attribute.items()))
        for option in attribute:
            if option.tag == METAMODEL_NAMESPACE + 'Enum':
                obj.AppendEnumValue(id, option.text)
            
            elif option.tag == METAMODEL_NAMESPACE + 'List':
                obj.SetList(id, **self.__LoadList(option))
                ltype = obj.GetAttribute(id)['list']['type']
                if ltype == 'list':
                    raise DomainFactoryError('List of lists not supported in "%s.%s"'
                        %(obj.GetName(), id))
                elif ltype is not None and '.' in ltype:
                    raise DomainFactoryError('Local domain "%s" cannot be used as explicitly '
                        'set itemtype of "%s.%s"' % (type, obj.GetName(), id))
            elif option.tag == METAMODEL_NAMESPACE + 'Domain':
                name = obj.GetName() +'.' + id
                self.__LoadDomain(option, name)
                obj.AppendImport(name)
                at = obj.GetAttribute(id)
                attype = at['type']
                if attype is None:
                    obj.GetAttribute(id)['type'] = name
                elif attype == 'list' and ('list' not in at or at['list']['type'] is None):
                    obj.SetList(id, type = name)
                else:
                    raise DomainFactoryError('Nested Domain "%s" is not allowed '
                        'because type is explicitly set.'%(name,))
    
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
