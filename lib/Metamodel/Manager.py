from lib.Depend.etree import etree, HAVE_LXML

from lib.Exceptions.DevException import *
from lib.config import config
from lib.Storages import open_storage
from Metamodel import CMetamodel
import os.path
from lib.consts import ROOT_PATH, METAMODEL_PATH, METAMODEL_LIST_NAMESPACE

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(config['/Paths/Schema'], "metamodel.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)

class CMetamodelManager(object):
    def __init__(self):
        self.__metamodels = {}
        self.__LoadList(config['/Paths/MetamodelList'])
    
    def GetMetamodel(self, uri, version):
        storage = open_storage(self.__metamodels[(uri, version)])
        return self.__LoadMetamodel(storage)
    
    def __LoadList(self, path):
        print path
        root = etree.XML(file(path).read())
        
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
                    path = info.text.replace(u'\xFF', ROOT_PATH)
            self.__metamodels[(uri, version)] = path
    
    def __LoadMetamodel(self, storage):
        metamodel = CMetamodel(storage)
        
        root = etree.XML(storage.read_file(METAMODEL_PATH))
        #xml (version) file is validate with xsd schema (metamodel.xsd)
        if HAVE_LXML:
            if not xmlschema.validate(root):
                raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        #Iterate over the descendants of root element (only element with tag=Item)
        for element in root[0]:
            diagName = element.get('value')
            metamodel.AddDiagram(diagName)
        
        return metamodel
