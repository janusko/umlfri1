from lib.Depend.libxml import etree
from lib.Base import CBaseObject

import os
import os.path

from lib.Domains.Object import CDomainObject
from lib.Exceptions.DevException import *
from Type import CConnectionType
from Alias import CConnectionAlias
from lib.consts import METAMODEL_NAMESPACE
from lib.Drawing.Objects import ALL, ALL_CONNECTION, CContainer, CSimpleContainer
from lib.Drawing.Context import BuildParam
from lib.Distconfig import SCHEMA_PATH

import weakref

xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "metamodel.xsd"))
xmlschema = etree.XMLSchema(xmlschema_doc)


class CConnectionFactory(CBaseObject):
    """
    Creates connection types from metamodel XMLs
    """
    def __init__(self, metamodel, storage, path, domainfactory):
        """
        Parse metamodel XMLs and creates connection types
        
        @param storage: Storage in which is file located
        @type  storage: L{CAbstractStorage<lib.Storages.AbstractStorage.CAbstractStorage>}
        
        @param path: Path to directory with connection metamodel XMLs
        @type path: string
        """
        self.types = {}
        self.path = path
        self.domainfactory = domainfactory
        self.metamodel = weakref.ref(metamodel)
        
        self.storage = storage
        for file in storage.listdir(self.path):
            if file.endswith('.xml'):
                self.__Load(os.path.join(self.path, file))

    def GetConnection(self, type):
        """
        Gets connection type by its name
        
        @param type: Name of connection type
        @type  type: string
        
        @return: Connection type of given name
        @rtype:  L{CConnectionType<Type.CConnectionType>}
        """
        if not type in self.types:
            raise FactoryError('unrecognized connectionType name "%s"' % type)
        return self.types[type]
    
    def IterTypes(self):
        '''
        iterator over connection types
        
        @rtype: L{CConnectionType<CConnectionType>}
        '''
        for type in self.types.itervalues():
            yield type
            
    def __Load(self, file_path):
        """
        Load an XMLs from given path
        
        @param file_path: Path to connections metamodel (within storage)
        @type  file_path: string
        """
        
        root = etree.XML(self.storage.read_file(file_path))

        #xml (version) file is validate with xsd schema (metamodel.xsd)
        if not xmlschema.validate(root):
            raise FactoryError("XMLError", xmlschema.error_log.last_error)

        if root.tag == METAMODEL_NAMESPACE + 'ConnectionType':
            self.__LoadType(root)
        elif root.tag == METAMODEL_NAMESPACE + 'ConnectionAlias':
            self.__LoadAlias(root)
    
    def __LoadAlias(self, root):
        obj = CConnectionAlias(self, root.get('id'), root.get('alias'))
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE + 'Icon':
                obj.SetIcon(element.get('path'))
            
            elif element.tag == METAMODEL_NAMESPACE + 'DefaultValues':
                for item in element:
                    obj.SetDefaultValue(item.get('path'), item.get('value'))
        
        self.types[root.get('id')] = obj
    
    def __LoadType(self, root):
        id = root.get('id')
        
        sarr = {}
        darr = {}
        ls = {}
        icon = None
        labels = []
        attrs = []
        domain = None
        identity = None
        visualObj = CContainer()
        domainId = None
        for element in root:
            if element.tag == METAMODEL_NAMESPACE+'Icon':
                icon = element.get('path')
            elif element.tag == METAMODEL_NAMESPACE+'Domain':
                domainId = element.get('id')
                domain = self.domainfactory.GetDomain(domainId)
                identity = element.get('identity')
            elif element.tag == METAMODEL_NAMESPACE+'Appearance':
                for child in element:
                    if root and child.tag == METAMODEL_NAMESPACE+'Label':
                        labels.append((child.get('position'), self.__LoadLabelAppearance(child[0], domain, domainId)))
                    else:
                        visualObj.AppendChild(self.__LoadAppearance(child, domain, domainId))

        tmp = self.types[id] = CConnectionType(self, id, visualObj, icon, domain, identity)
        for pos, lbl in labels:
            tmp.AddLabel(pos, lbl)
    
    def __LoadAppearance(self, root, domainType, subDomainId, vars={}):
        """
        Loads an appearance section of an XML file
        
        @param root: Visual object XML definition
        @type  root: L{Element<lxml.etree.Element>}
        
        @return: Visual object representing this section
        @rtype:  L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}
        """
        
        tagName = root.tag.split("}")[1]
        
        if tagName not in ALL_CONNECTION:
            raise FactoryError("XMLError", root.tag)
        
        cls = ALL_CONNECTION[tagName]
        
        params = {}
        subdomain = domainType
        localvars = vars
        for attr in root.attrib.items():
            pomstr = attr[1]
            if pomstr.startswith('#'):
                if pomstr.startswith('#self.'):
                    newSubdomainId = pomstr[6:]
                else:
                    newSubdomainId = pomstr[1:]
                try:
                    subdomain = self.domainfactory.GetDomain(subDomainId+'.'+newSubdomainId)
                    subDomainId = subDomainId + '.' + newSubdomainId
                    localvars.update(subdomain.GetAttributeTypes(subDomainId, self.domainfactory))
                except Exception as e:
                    #print e
                    pass

            params[attr[0]] = BuildParam(attr[1], domainType, localvars, cls.types.get(attr[0], None))
        ret = obj = cls(**params)
        
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            if len(root) > 1 and isinstance(obj, CSimpleContainer):
                tmp = CContainer()
                obj.SetChild(tmp)
                obj = tmp
            for child in root:
                obj.AppendChild(self.__LoadAppearance(child, domainType, subDomainId, localvars))
        return ret
    
    def __LoadLabelAppearance(self, root, domainType, subDomainId, vars={}):
        """
        Loads the label from an appearance section of an XML file
        
        @param root: Label element child
        @type  root: L{Element<lxml.etree.Element>}
        
        @return: Visual object representing this section
        @rtype:  L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}
        """

        if root.tag.split("}")[1] not in ALL:
            raise FactoryError("XMLError", root.tag)
        
        cls = ALL[root.tag.split("}")[1]]
        params = {}
        subdomain = domainType
        localvars = vars
        for attr in root.attrib.items():
            pomstr = attr[1]
            if pomstr.startswith('#'):
                if pomstr.startswith('#self.'):
                    newSubdomainId = pomstr[6:]
                else:
                    newSubdomainId = pomstr[1:]
                try:
                    subdomain = self.domainfactory.GetDomain(subDomainId+'.'+newSubdomainId)
                    subDomainId = subDomainId + '.' + newSubdomainId
                    localvars.update(subdomain.GetAttributeTypes(subDomainId, self.domainfactory))
                except Exception as e:
                    #print e
                    pass

            params[attr[0]] = BuildParam(attr[1], domainType, localvars, cls.types.get(attr[0], None))
        obj = cls(**params)
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            for child in root:
                obj.AppendChild(self.__LoadLabelAppearance(child, domainType, subDomainId, localvars))
        return obj
    
    def GetMetamodel(self):
        return self.metamodel()
