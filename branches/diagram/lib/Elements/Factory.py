import os
import os.path
from lib.Exceptions.DevException import *
from Type import CElementType
from Alias import CElementAlias
from lib.config import config
from lib.consts import METAMODEL_NAMESPACE
from lib.Drawing.Objects import ALL
from lib.Drawing.Context import BuildParam
from lib.Generic import CGenericFactory

class CElementFactory(CGenericFactory):
    """
    Factory, that creates element type objects
    """
    
    def Load(self, root):
        """
        Load an XMLs from given path
        """
        if root.tag == METAMODEL_NAMESPACE + 'ElementType':
            self.__LoadType(root)
        elif root.tag == METAMODEL_NAMESPACE + 'ElementAlias':
            self.__LoadAlias(root)
    
    def __LoadAlias(self, root):
        obj = CElementAlias(self, root.get('id'), root.get('alias'))
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE + 'Icon':
                obj.SetIcon(element.get('path'))
            
            elif element.tag == METAMODEL_NAMESPACE + 'DefaultValues':
                for item in element:
                    obj.SetDefaultValue(item.get('path'), item.get('value'))
            
            elif element.tag == METAMODEL_NAMESPACE + 'Options':
                for item in element:
                    name = item.tag.split('}')[1]
                    value = item.text
                    if name == 'DirectAdd':
                        value = value.lower() == 'true'
                    obj.AppendOptions(name, value)
        
        self._AddType(root.get('id'), obj)
    
    def __LoadType(self, root):
        obj = CElementType(root.get('id'))
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE + 'Icon':
                obj.SetIcon(element.get('path'))
            
            elif element.tag == METAMODEL_NAMESPACE + 'Domain':
                obj.SetDomain(self.domainfactory.GetDomain(element.get('id')))
                obj.SetIdentity(element.get('identity'))
            
            elif element.tag == METAMODEL_NAMESPACE+'Connections':
                self.__LoadConnections(obj, element)
                
            elif element.tag == METAMODEL_NAMESPACE+'Appearance':
                tmp = None
                for j in element:
                    tmp = j
                obj.SetAppearance(self.__LoadAppearance(tmp))
            elif element.tag == METAMODEL_NAMESPACE+'Options':
                for item in element:
                    name = item.tag.split('}')[1]
                    value = item.text
                    if name == 'DirectAdd':
                        value = value.lower() == 'true'
                    obj.AppendOptions(name, value)
        
        self._AddType(root.get('id'), obj)
    
    def __LoadAppearance(self, root):
        """
        Loads an appearance section of an XML file
        
        @param root: Appearance element
        @type  root: L{Element<lxml.etree.Element>}
        
        @return: Visual object representing this section
        @rtype:  L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}
        """
        if root.tag.split("}")[1] not in ALL:
            raise FactoryError("XMLError", root.tag)
        cls = ALL[root.tag.split("}")[1]]
        params = {}
        for attr in root.attrib.items():    #return e.g. attr == ('id', '1') => attr[0] == 'id', attr[1] == '1'
            params[attr[0]] = BuildParam(attr[1], cls.types.get(attr[0], None))
        obj = cls(**params)
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            for child in root:
                obj.AppendChild(self.__LoadAppearance(child))
        return obj
    
    def __LoadConnections(self, obj, root):
        for item in root:
            value = item.get('value')
            with_what = None
            allow_recursive = False
            if item.get('with') != None:
                with_what = item.get('with').split(',')
            if item.get('allowrecursive') != None:
                allow_recursive = item.get('allowrecursive').lower() in ('1', 'true', 'yes')
            obj.AppendConnection(value, with_what, allow_recursive)
