from Depend.etree import etree, HAVE_LXML, XMLSyntaxError

import consts
import os.path
import os
import colors
from lib import Indent
from Exceptions.DevException import *
from Exceptions import XMLError
from datatypes import CFont, CColor
import sys

def expanduser(path):
    if path[0] == '~':
        return os.path.expanduser('~').decode(sys.getfilesystemencoding()) + path[1:]
    return path

def path_type(val):
    val = val.replace(u'\xFF', consts.ROOT_PATH)
    val = os.path.abspath(expanduser(val))
    if os.path.isdir(val):
        val += os.sep
    return val

types = {
    "/Styles/Element/LineColor": CColor,
    "/Styles/Element/FillColor": CColor,
    "/Styles/Element/Fill2Color": CColor,
    "/Styles/Element/Fill3Color": CColor,
    "/Styles/Element/ShadowColor": CColor,
    "/Styles/Element/NameTextColor": CColor,
    "/Styles/Element/TextColor": CColor,
    "/Styles/Element/NameTextFont": CFont,
    "/Styles/Element/Textfont": CFont,
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
    "/Paths/Root": path_type,
    "/Paths/MetamodelList": path_type,
    "/Paths/Templates": path_type,
    "/Paths/Images": path_type,
    "/Paths/Gui": path_type,
    "/Paths/Locales": path_type,
    "/Paths/Schema": path_type,
    "/Paths/UserDir": path_type,
    "/Paths/UserConfig": path_type,
    "/Paths/UserMetamodelList": path_type,
    "/Paths/RecentFiles": path_type,
    "/Paths/UserGui": path_type,
    "/Paths/Plugins": path_type,
    "/Page/Width": int,
    "/Page/Height": int,
}

class CConfig(object):
    """
    Automatic config file manager
    """
    
    CONFIG_NAMESPACE = 'http://umlfri.kst.fri.uniza.sk/xmlschema/config.xsd'
    USERCONFIG_NAMESPACE = 'http://umlfri.kst.fri.uniza.sk/xmlschema/userconfig.xsd'
    
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
            xmlschema_path = path_type(tree.find('./{'+self.CONFIG_NAMESPACE+'}Paths/{'+self.CONFIG_NAMESPACE+'}Schema').text)
            if not xmlschema_path:
                raise Exception, ("XMLError", "Schema path is not found in config file")
            xmlschema_doc = etree.parse(os.path.join(xmlschema_path, "config.xsd"))
            xmlschema = etree.XMLSchema(xmlschema_doc)
            if not xmlschema.validate(tree):
                raise ConfigError, ("XMLError", xmlschema.error_log.last_error)
        
        self.original = self.__Load(tree)
        self.cfgs = self.original.copy()
        
        k = self.original.keys()
        k.sort()
        
        if not os.path.isdir(self['/Paths/UserDir']):
            os.mkdir(self['/Paths/UserDir'])

        if HAVE_LXML:
            xmlschema_doc = etree.parse(os.path.join(xmlschema_path, "userconfig.xsd"))
            self.xmlschema = etree.XMLSchema(xmlschema_doc)

        try:
            self.file = self['/Paths/UserConfig']
            if os.path.isfile(self.file):
                tree = etree.XML(open(self.file).read())
                if HAVE_LXML:
                    if not self.xmlschema.validate(tree):
                        raise ConfigError, ("XMLError", self.xmlschema.error_log.last_error)
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
        save = {'Config': out}
        f = file(self.file, 'w')
        
        def save(root = save['Config'], node = None, level = 1):
            for part, val in root.iteritems():
                newNode = etree.Element('{%s}%s'%(self.USERCONFIG_NAMESPACE, part))
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
        
        rootNode = etree.XML('<Config xmlns="%s"></Config>'%self.USERCONFIG_NAMESPACE)
        save(node = rootNode)
        
        #xml tree is validate with xsd schema (recentfile.xsd)
        if HAVE_LXML:
            if not self.xmlschema.validate(rootNode):
                raise ConfigError, ("XMLError", self.xmlschema.error_log.last_error)
        
        #make human-friendly tree
        Indent(rootNode)
        
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

config = CConfig(consts.MAIN_CONFIG_PATH)
