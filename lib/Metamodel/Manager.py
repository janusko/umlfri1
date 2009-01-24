from lib.Depend.etree import etree, HAVE_LXML

from lib.Exceptions.DevException import *
from lib.config import config
from lib.Storages import open_storage
from Metamodel import CMetamodel
import os.path
from lib.consts import ROOT_PATH, METAMODEL_PATH

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(config['/Paths/Schema'], "metamodel.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)

class CMetamodelManager(object):
    def __init__(self):
        pass
    
    def GetMetamodel(self, uri, version):
        storage = open_storage(os.path.join(ROOT_PATH, 'etc', 'uml'))
        return self.__LoadMetamodel(storage)
    
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
