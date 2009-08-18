from lib.Depend.etree import etree, HAVE_LXML

import re
import os
import os.path
import uuid

from lib.lib import Indent
from lib.Storages import open_storage, CDirectory
from Addon import CAddon
from Metamodel import CMetamodelAddonComponent
from lib.consts import ADDON_NAMESPACE, ADDON_LIST_NAMESPACE, ADDON_PATH
from lib.config import config

from lib.Exceptions.DevException import *

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(config['/Paths/Schema'], "addon.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xmlschema_list_doc = etree.parse(os.path.join(config['/Paths/Schema'], "addonList.xsd"))
    xmlschema_list = etree.XMLSchema(xmlschema_list_doc)

class CAddonManager(object):
    reSpaces = re.compile(' +')
    reIlegalCharacters = re.compile('[^a-z0-9A-Z]')
    
    def __init__(self):
        self.__enabledAddons = self.__LoadEnabledAddons(config['/Paths/UserEnabledAddons'])
        self.__addons = self.__LoadAllAddons(open_storage(config['/Paths/Addons']), False)
        self.__addons.update(self.__LoadAllAddons(open_storage(config['/Paths/UserAddons']), True))
    
    def __LoadEnabledAddons(self, path):
        ret = {}
        
        if not os.path.exists(path):
            return ret
        
        root = etree.XML(file(path).read())
        if HAVE_LXML:
            if not xmlschema_list.validate(root):
                raise FactoryError("XMLError", xmlschema_list.error_log.last_error)
        
        for node in root:
            ret[node.attrib['uri']] = node.attrib.get('enabled', 'true').lower() in ('true', 'yes', '1')
        
        return ret
    
    def __SaveEnabledAddons(self, path, values):
        root = etree.XML("<AddOns xmlns=\"%s\"/>"%ADDON_LIST_NAMESPACE[1:-1])
        
        for uri, enabled in values.iteritems():
            root.append(etree.Element(ADDON_LIST_NAMESPACE+"AddOn", uri = uri, enabled = str(int(enabled))))
        
        if HAVE_LXML:
            if not xmlschema_list.validate(root):
                raise FactoryError("XMLError", xmlschema_list.error_log.last_error)
        
        f = file(path, 'w')
        
        #make human-friendly tree
        Indent(root)
        
        print>>f, '<?xml version="1.0" encoding="utf-8"?>'
        print>>f, etree.tostring(root, encoding='utf-8')
    
    def __LoadAllAddons(self, storage, uninstallable):
        tmp = {}
        
        if storage is None:
            return tmp
        
        for addon in storage.listdir('.'):
            if addon.startswith('.'):
                continue
            
            addonStorage = storage.subopen(addon)
            if addonStorage is not None:
                tmp.update(self.__LoadAddonToDict(addonStorage, uninstallable))
        
        return tmp
    
    def __LoadAddonToDict(self, storage, uninstallable):
        tmp = {}
        
        addon = self.__LoadAddon(storage, uninstallable)
        if addon is not None:
            for uri in addon.GetUris():
                tmp[uri] = addon
        
        return tmp
    
    def __LoadAddon(self, storage, uninstallable):
        if not storage.exists(ADDON_PATH):
            return None
        
        root = etree.XML(storage.read_file(ADDON_PATH))
        if HAVE_LXML:
            if not xmlschema.validate(root):
                raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        uris = []
        name = None
        version = None
        component = None
        icon = None
        description = None
        author = []
        license = None, None
        homepage = None
        
        for node in root:
            if node.tag == ADDON_NAMESPACE+'Identity':
                uris.append(node.attrib["uri"])
            elif node.tag == ADDON_NAMESPACE+'FriendlyName':
                name = node.attrib["name"]
                version = node.attrib.get("version")
            elif node.tag == ADDON_NAMESPACE+'Author':
                for info in node:
                    if info.tag == ADDON_NAMESPACE+'Name':
                        author.append(info.attrib["name"])
                    elif info.tag == ADDON_NAMESPACE+'Homepage':
                        homepage = info.attrib["url"]
                    elif info.tag == ADDON_NAMESPACE+'CommonLicense':
                        if "file" in info.attrib:
                            license = info.attrib["name"], storage.read_file(info.attrib["file"])
                        else:
                            license = info.attrib["name"], None
                    elif info.tag == ADDON_NAMESPACE+'License':
                        license = None, info.text
                    elif info.tag == ADDON_NAMESPACE+'ExternalLicense':
                        license = None, storage.read_file(info.attrib["file"])
            elif node.tag == ADDON_NAMESPACE+'Icon':
                icon = node.attrib["path"]
            elif node.tag == ADDON_NAMESPACE+'Description':
                description = self.__FormatMultilineText(node.text)
            elif node.tag == ADDON_NAMESPACE+'Metamodel':
                path = ''
                for info in node:
                    if node.tag == ADDON_NAMESPACE+'Path':
                        path = node.attrib["icon"]
                component = CMetamodelAddonComponent(path)
        
        return CAddon(self, storage, uris, component,
            all(self.__enabledAddons.get(uri, True) for uri in uris),
            uninstallable, author, name, version, license, homepage,
            icon, description)
    
    def __FormatMultilineText(self, text):
        ret = []
        buf = []
        for line in text.splitlines():
            line = self.reSpaces.sub(' ', line.strip())
            if line:
                buf.append(line)
            elif buf:
                ret.append(' '.join(buf))
                buf = []
        return '\n'.join(ret)
    
    def _RefreshAddonEnabled(self, addon):
        for uri in addon.GetUris():
            if uri in self.__enabledAddons:
                del self.__enabledAddons[uri]
        
        self.__enabledAddons[addon.GetDefaultUri()] = addon.IsEnabled()
    
    def _DeleteAddon(self, addon):
        for uri in addon.GetUris():
            if uri in self.__enabledAddons:
                del self.__enabledAddons[uri]
            del self.__addons[uri]
    
    def GetAddon(self, uri):
        if uri in self.__addons:
            return self.__addons[uri]
        else:
            return None
    
    def ListAddons(self, type = None):
        if type is None:
            l = self.__addons.values()
        else:
            l = [addon for addon in self.__addons.itervalues() if addon.GetType() == type]
        l = list(set(l))
        l.sort(key = lambda x: x.GetName())
        for addon in l:
            yield addon
    
    def Save(self):
        self.__SaveEnabledAddons(config['/Paths/UserEnabledAddons'], self.__enabledAddons)
    
    def LoadAddon(self, path):
        return self.__LoadAddon(open_storage(path), False)
    
    def InstallAddon(self, addon):
        dirname = str(uuid.uuid5(uuid.NAMESPACE_URL, addon.GetDefaultUri()))
        path = os.path.join(config['/Paths/UserAddons'], dirname)
        storage = CDirectory.duplicate(addon.GetStorage(), path)
        
        self.__addons.update(self.__LoadAddonToDict(storage, True))
