from lib.Depend.libxml import etree

import os
import os.path
from lib.Exceptions.DevException import *
from Type import CDiagramType
from lib.Distconfig import SCHEMA_PATH
from lib.consts import METAMODEL_NAMESPACE
import weakref
from lib.Base import CBaseObject

xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "metamodel.xsd"))
xmlschema = etree.XMLSchema(xmlschema_doc)

class CDiagramFactory(CBaseObject):
    """
    Creates diagram types from metamodel XMLs
    """
    def __init__(self, metamodel, storage, path, domainfactory):
        """
        Parse metamodel and create list of diagram types
        
        @param storage: Storage in which is file located
        @type  storage: L{CAbstractStorage<lib.Storages.AbstractStorage.CAbstractStorage>}
        
        @param path: Path to directory with diagram metamodel XMLs
        @type  path: string
        
        @param domainfactory: factory that has already loaded all the domains
        from current metamodel
        @type domainfactory: L{CDomainFactory<lib.Domains.Factory.CDomainFactory>}
        """
        self.types = {}
        self.path = path
        self.storage = storage
        self.metamodel = weakref.ref(metamodel)
        self.domainfactory = weakref.ref(domainfactory)
        self.Reload()
        
    def GetDiagram(self, type):
        """
        Get diagram type by its name
        
        @param type: diagram type name
        @type  type: string
        
        @return: Diagram type of given name
        @rtype: L{CDiagramType<lib.Diagrams.Type.CDiagramType>}
        """
        if self.types.has_key(type):
            return self.types[type]
        else:
            raise FactoryError("KeyError")
    
    def Reload(self):
        """
        Reload diagrams metamodel
        """
        for file in self.storage.listdir(self.path):
            if file.endswith('.xml'):
                self.__Load(os.path.join(self.path, file))
    
    def HasType(self, id):
        return id in self.types
    
    def __iter__(self):
        """
        Iterator over all contained diagram types
        
        @return: diagram types
        @rtype:  iterator over L{CDiagramType<lib.Diagrams.Type.CDiagramType>}(s)
        """
        for i in self.types.values():
            yield i
        
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

        obj = CDiagramType(self, root.get('id'))
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE+'Icon':
                obj.SetIcon(element.get('path'))
                
            elif element.tag == METAMODEL_NAMESPACE+'Special':
                swimlines = element.get('swimlines')
                lifelines = element.get('lifelines')
                obj.SetSpecial(swimlines, lifelines)
           
            elif element.tag == METAMODEL_NAMESPACE + 'Domain':
                obj.SetDomain(self.domainfactory().GetDomain(element.get('id')))
                obj.SetIdentity(element.get('identity'))
                
            elif element.tag == METAMODEL_NAMESPACE+'Elements':
                for item in element:
                    if item.tag == METAMODEL_NAMESPACE+'Item':
                        value = item.get('value')
                        obj.AppendElement(value)
                    
            elif element.tag == METAMODEL_NAMESPACE+'Connections':
                for item in element:
                    if item.tag == METAMODEL_NAMESPACE+'Item':
                        value = item.get('value')
                        obj.AppendConnection(value)
        
        self.types[root.get('id')] = obj
    
    def GetMetamodel(self):
        return self.metamodel()
    