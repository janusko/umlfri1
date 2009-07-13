import os
import os.path
from lib.Exceptions.DevException import *
from Type import CConnectionType
from Alias import CConnectionAlias
from lib.consts import METAMODEL_NAMESPACE
from lib.Drawing.Objects import ALL, ALL_CONNECTION, CContainer, CSimpleContainer
from lib.Drawing.Context import BuildParam
from lib.config import config
from lib.Generic import CGenericFactory

class CConnectionFactory(CGenericFactory):
    """
    Creates connection types from metamodel XMLs
    """
    
    def Load(self, root):
        """
        Load an XMLs from given path
        
        @param file_path: Path to connections metamodel (within storage)
        @type  file_path: string
        """
        
        if root.tag == METAMODEL_NAMESPACE + 'ConnectionType':
            self.__LoadType(root)
        elif root.tag == METAMODEL_NAMESPACE + 'ConnectionAlias':
            self.__LoadAlias(root)
    
    
    def __LoadAlias(self, root):
        obj = CConnectionAlias(self, root.get('id'), root.get('alias'))
        self._AddType(root.get('id'), obj)
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE + 'Icon':
                obj.SetIcon(element.get('path'))
            
            elif element.tag == METAMODEL_NAMESPACE + 'DefaultValues':
                for item in element:
                    obj.SetDefaultValue(item.get('path'), item.get('value'))
        
    
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
        for element in root:
            if element.tag == METAMODEL_NAMESPACE+'Icon':
                icon = element.get('path')
            elif element.tag == METAMODEL_NAMESPACE+'Domain':
                domain = self.domainfactory.GetDomain(element.get('id'))
                identity = element.get('identity')
            elif element.tag == METAMODEL_NAMESPACE+'Appearance':
                for child in element:
                    if root and child.tag == METAMODEL_NAMESPACE+'Label':
                        labels.append((child.get('position'), self.__LoadLabelAppearance(child[0])))
                    else:
                        visualObj.AppendChild(self.__LoadAppearance(child))
        obj = CConnectionType(id, visualObj, icon, domain, identity)
        self._AddType(root.get('id'), obj)
        for pos, lbl in labels:
            obj.AddLabel(pos, lbl)
    
    def __LoadAppearance(self, root):
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
        for attr in root.attrib.items():
            params[attr[0]] = BuildParam(attr[1], cls.types.get(attr[0], None))
        ret = obj = cls(**params)
        
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            if len(root) > 1 and isinstance(obj, CSimpleContainer):
                tmp = CContainer()
                obj.SetChild(tmp)
                obj = tmp
            for child in root:
                obj.AppendChild(self.__LoadAppearance(child))
        return ret
    
    def __LoadLabelAppearance(self, root):
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
        for attr in root.attrib.items():
            params[attr[0]] = BuildParam(attr[1], cls.types.get(attr[0], None))
        obj = cls(**params)
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            for child in root:
                obj.AppendChild(self.__LoadLabelAppearance(child))
        return obj
