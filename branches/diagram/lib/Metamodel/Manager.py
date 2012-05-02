from lib.Depend.etree import etree, HAVE_LXML

from lib.Exceptions.DevException import *
from lib.config import config
from lib.Storages import open_storage
from Metamodel import CMetamodel
import os.path
from lib.consts import ROOT_PATH, METAMODEL_PATH, METAMODEL_NAMESPACE, METAMODEL_LIST_NAMESPACE

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(config['/Paths/Schema'], "metamodel.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)

class CMetamodelManager(object):
    def __init__(self):
        self.__metamodels = {}
        self.__metamodels.update(self.__LoadList(file(config['/Paths/MetamodelList'])))
        if os.path.exists(config['/Paths/UserMetamodelList']):
            self.__metamodels.update(self.__LoadList(file(config['/Paths/UserMetamodelList'])))
    
    def GetMetamodel(self, uri, version, project_file = None):
        if project_file is not None:
            storage = open_storage(project_file)
            if storage and storage.exists('metamodels.xml'):
                metamodels = self.__LoadList(storage.file('metamodels.xml'))
                if (uri, version) in metamodels:
                    storage = open_storage(os.path.join(project_file, metamodels[(uri, version)]))
                    return self.__LoadMetamodel(storage)
        storage = open_storage(self.__metamodels[(uri, version)])
        return self.__LoadMetamodel(storage)
    
    def __LoadList(self, file):
        root = etree.XML(file.read())
        metamodels = {}
        
        for node in root:
            uri = None
            version = None
            path = None
            for info in node:
                if info.tag == METAMODEL_LIST_NAMESPACE+'Uri':
                    uri = info.text
                elif info.tag == METAMODEL_LIST_NAMESPACE+'Version':
                    version = info.text
                elif info.tag == METAMODEL_LIST_NAMESPACE+'Path':
                    path = os.path.expanduser(info.text.replace(u'\xFF', ROOT_PATH))
            metamodels[(uri, version)] = path
        return metamodels
    
    def __LoadMetamodel(self, storage):
        root = etree.XML(storage.read_file(METAMODEL_PATH))
        #xml (version) file is validate with xsd schema (metamodel.xsd)
        if HAVE_LXML:
            if not xmlschema.validate(root):
                raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        for info in root[0]:
            if info.tag == METAMODEL_NAMESPACE+'Uri':
                uri = info.text
            elif info.tag == METAMODEL_NAMESPACE+'Version':
                version = info.text
        
        metamodel = CMetamodel(storage, uri, version)
        
        #Iterate over the descendants of root element (only element with tag=Item)
        for element in root[1]:
            diagName = element.get('value')
            metamodel.AddDiagram(diagName)
        
        return metamodel
