from lib.Depend.libxml import etree

from lib.Distconfig import SCHEMA_PATH
from lib.Math2D import Path
from lib.consts import METAMODEL_NAMESPACE

import os.path

xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "metamodel.xsd"))
xmlschema = etree.XMLSchema(xmlschema_doc)

class CPathFactory(object):
    def __init__(self, storage, path):
        self.storage = storage
        self.paths = {}
        
        root = etree.XML(self.storage.read_file(path))

        #xml (version) file is validate with xsd schema (metamodel.xsd)
        if not xmlschema.validate(root):
            raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE + 'Path':
                self.paths[element.get('id')] = Path(element.get('path'))
    
    def GetPath(self, id):
        return self.paths[id]
    
