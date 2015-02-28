import weakref
import os.path

from lib.Depend.libxml import etree

from lib.Exceptions.DevException import *
from lib.Distconfig import SCHEMA_PATH

from Metamodel import CMetamodel

xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "metamodel.xsd"))
xmlschema = etree.XMLSchema(xmlschema_doc)

class CMetamodelAddonComponent(object):
    def __init__(self, path, templates):
        self.__path = path
        self.__addon = None
        self.__metamodel = None
        self.__templates = templates
    
    def _SetAddon(self, addon):
        self.__addon = addon
    
    def LoadMetamodel(self):
        if not self.__addon.IsEnabled():
            return None
        
        if self.__metamodel == None:
            storage = self.__addon.GetStorage().subopen(self.__path)
            
            root = etree.XML(storage.read_file('metamodel.xml'))
            #xml (version) file is validate with xsd schema (metamodel.xsd)
            if not xmlschema.validate(root):
                raise FactoryError("XMLError", xmlschema.error_log.last_error)
            
            self.__metamodel = CMetamodel(storage, self.__addon.GetDefaultUri(), self.__addon.GetVersion())
            
            #Iterate over the descendants of root element (only element with tag=Item)
            for element in root[0]:
                diagName = element.get('value')
                self.__metamodel.AddDiagram(diagName)
                
            diagramIds = []
            for diagram in (self.__metamodel.GetDiagramFactory()).types.values():
                diagramIds.append(diagram.id)
            for diagram in self.__metamodel.GetDiagrams():
                if diagram not in diagramIds:
                    raise FactoryError("Unsupported diagram type: " + diagram)
        return self.__metamodel
    
    def GetTemplates(self):
        for name, icon, path in self.__templates:
            yield name, icon, path
    
    def GetType(self):
        return 'metamodel'
    
    def Start(self):
        pass
    
    def Stop(self):
        pass
    
    def Terminate(self):
        pass
        
    def Kill(self):
        pass
        
    def IsRunning(self):
        return self.__addon.IsEnabled()
    
    def GetRunInProcess(self):
        return False
