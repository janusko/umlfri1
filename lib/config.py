from __future__ import with_statement

from Depend.etree import etree, HAVE_LXML, XMLSyntaxError

from Distconfig import SCHEMA_PATH, CONFIG_PATH, USERDIR_PATH

from consts import CONFIG_NAMESPACE, USERCONFIG_NAMESPACE
from lib import Indent
from Exceptions.DevException import *
from Exceptions import XMLError
from datatypes import CFont, CColor
from Base import CBaseObject

import os.path
import os

types = {
    "/Styles/Element/LineColor": CColor,
    "/Styles/Element/FillColor": CColor,
    "/Styles/Element/Fill2Color": CColor,
    "/Styles/Element/Fill3Color": CColor,
    "/Styles/Element/ShadowColor": CColor,
    "/Styles/Element/NameTextColor": CColor,
    "/Styles/Element/TextColor": CColor,
    "/Styles/Element/NameTextFont": CFont,
    "/Styles/Element/TextFont": CFont,
    "/Styles/Connection/ArrowAngleSteps": int,
    "/Styles/Connection/MinimalAngle": float,
    "/Styles/Connection/LineColor": CColor,
    "/Styles/Connection/ArrowColor": CColor,
    "/Styles/Connection/ArrowFillColor": CColor,
    "/Styles/Connection/NameTextColor": CColor,
    "/Styles/Connection/TextColor": CColor,
    "/Styles/Connection/TextFill": CColor,
    "/Styles/Connection/NameTextFont": CFont,
    "/Styles/Connection/Textfont": CFont,
    "/Styles/Selection/PointsSize": int,
    "/Styles/Selection/RectangleWidth": int,
    "/Styles/Selection/PointsColor": CColor,
    "/Styles/Selection/RectangleColor": CColor,
    "/Styles/Drag/RectangleWidth": int,
    "/Styles/Drag/RectangleColor": CColor,
    "/Grid/LineColor1": CColor,
    "/Grid/LineColor2": CColor,
    "/Grid/Active": bool,
    "/Grid/Visible": bool,
    "/Grid/HorSpacing": int,
    "/Grid/VerSpacing": int,
    "/Grid/LineWidth": float,
    "/Grid/SnapMode": str,
    "/Page/Width": int,
    "/Page/Height": int,
}

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "config.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    xmlschema_user_doc = etree.parse(os.path.join(SCHEMA_PATH, "userconfig.xsd"))
    xmlschema_user = etree.XMLSchema(xmlschema_user_doc)

class CConfig(CBaseObject):
    """
    Automatic config file manager
    """
    
    def __init__(self, file):
        """
        Initialize config manager and loads config file
        
        @param file: path to config file
        @type  file: string
        """
        self.file = None
        self.original = {}
        self.Clear()
        
        tree = etree.XML(open(file).read())
        if HAVE_LXML:
            if not xmlschema.validate(tree):
                raise ConfigError, ("XMLError", xmlschema.error_log.last_error)
        
        self.original = self.__Load(tree)
        self.cfgs = self.original.copy()
        
        k = self.original.keys()
        k.sort()
        
        if not os.path.isdir(USERDIR_PATH):
            os.mkdir(USERDIR_PATH)

        try:
            self.file = os.path.join(USERDIR_PATH, 'config.xml')
            if os.path.isfile(self.file):
                tree = etree.XML(open(self.file).read())
                if HAVE_LXML:
                    if not xmlschema_user.validate(tree):
                        raise ConfigError, ("XMLError", xmlschema_user.error_log.last_error)
                self.cfgs.update(self.__Load(tree))
        except (XMLSyntaxError, ConfigError):
            print 'WARNING: Your local config file is malformed. Personal settings will be ignored'
            

    
    def Clear(self):
        """
        Clears the config values
        """
        self.cfgs = {}
        self.revision = 0
    
    def LoadDefaults(self):
        """
        Loads the default config values
        """
        self.cfgs = self.original.copy()
        self.revision += 1
    
    def __setitem__(self, path, value):
        """
        Set config value
        
        @param path: path to config value
        @type  path: string
        
        @param value: value to set
        @type  value: atomic
        """
        self.revision += 1
        self.cfgs[path] = value
    
    def __getitem__(self, path):
        """
        Get config value
        
        @param path: path to config value
        @type  path: string
        
        @return: value at given path
        @rtype:  atomic
        """
        return self.cfgs[path]
    
    def __contains__(self, path):
        """
        Determine, if given path exists in config
        
        @param path: path to config value
        @type  path: string
        
        @return: True, if path exists
        @rtype:  boolean
        """
        return path in self.cfgs
    
    def __Load(self, root):
        """
        Load an XML file under given path
        
        @param root: XML element to parse
        @type  root: L{Element<xml.etree.ElementTree.Element>}
        """
        
        ret = {}
        def recursive(root, path):
            for child in root:
                name = path+child.tag.split('}')[1]
                if len(child):
                    recursive(child, name+'/')
                elif child.text is None:
                    ret[name] = types.get(name, unicode)('')
                else:
                    ret[name] = types.get(name, unicode)(child.text)
        
        recursive(root, '/')
        
        return ret
    
    def Save(self):
        """
        Save changes to user config XML file
        """
        out = {}
        
        def save(root = out, node = None, level = 1):
            for part, val in root.iteritems():
                newNode = etree.Element('%s%s'%(USERCONFIG_NAMESPACE, part))
                if isinstance(val, dict):
                    save(val, newNode, level+1)
                else:
                    newNode.text = unicode(val)
                node.append(newNode)
        
        for path, val in self.cfgs.iteritems():
            if val != self.original.get(path, None):
                tmp = out
                path = path.split('/')
                for part in path[1:-1]:
                    tmp2 = tmp.setdefault(part, {})
                    if not isinstance(tmp2, dict):
                        tmp2 = tmp[part] = {}
                    tmp = tmp2
                tmp[path[-1]] = val
        
        rootNode = etree.XML('<Config xmlns="%s"></Config>'%USERCONFIG_NAMESPACE[1:-1])
        save(node = rootNode)
        
        #make human-friendly tree
        Indent(rootNode)
        
        #xml tree is validate with xsd schema (recentfile.xsd)
        if HAVE_LXML:
            if not xmlschema_user.validate(rootNode):
                if __debug__:
                    with open(self.file + '.error', 'w') as f:
                        print>>f, '<?xml version="1.0" encoding="utf-8"?>'
                        print>>f, etree.tostring(rootNode, encoding='utf-8')
                raise ConfigError, ("XMLError", xmlschema_user.error_log.last_error)
        
        with file(self.file, 'w') as f:
            print>>f, '<?xml version="1.0" encoding="utf-8"?>'
            print>>f, etree.tostring(rootNode, encoding='utf-8')
   
    def GetRevision(self):
        """
        Get revision number of config object. Revision is initiated to
        zero and incremented after each change
        
        @return: revision number
        @rtype:  integer
        """
        return self.revision

config = CConfig(CONFIG_PATH)
