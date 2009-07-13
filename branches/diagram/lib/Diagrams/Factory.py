import os
import os.path
from lib.Exceptions.DevException import *
from Type import CDiagramType
from lib.config import config
from lib.consts import METAMODEL_NAMESPACE
from lib.Generic import CGenericFactory

class CDiagramFactory(CGenericFactory):
    """
    Creates diagram types from metamodel XMLs
    """
        
    def Load(self, root):
        """
        Load an XMLs from given path
        
        @param file_path: Path to connections metamodel (within storage)
        @type  file_path: string
        """
        
        obj = CDiagramType(root.get('id'))
        self._AddType(root.get('id'), obj)
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE+'Icon':
                obj.SetIcon(element.get('path'))
                
            elif element.tag == METAMODEL_NAMESPACE+'Special':
                swimlines = element.get('swimlines')
                lifelines = element.get('lifelines')
                obj.SetSpecial(swimlines, lifelines)
                
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
    
