from lib.Depend.etree import etree, HAVE_LXML

import os
import os.path

from lib.Storages import open_storage
from Addon import CAddon
from Metamodel import CMetamodelAddonComponent
from lib.consts import ADDON_NAMESPACE, ADDON_PATH
from lib.config import config

class CAddonManager(object):
    def __init__(self):
        self.__addons = self.__LoadAllAddons(open_storage(config['/Paths/Addons']))
        self.__addons.update(self.__LoadAllAddons(open_storage(config['/Paths/UserAddons'])))
        
    def __LoadAllAddons(self, storage):
        tmp = {}
        
        if storage is None:
            return tmp
        
        for addon in storage.listdir('.'):
            addonStorage = storage.subopen(addon)
            if addonStorage is not None:
                addon = self.__LoadAddon(addonStorage)
                if addon is not None:
                    tmp[addon.GetUri()] = addon
        
        return tmp
    
    def __LoadAddon(self, storage):
        if not storage.exists(ADDON_PATH):
            return None
        
        root = etree.XML(storage.read_file(ADDON_PATH))
        
        uri = None
        name = None
        version = None
        component = None
        icon = None
        
        for node in root:
            if node.tag == ADDON_NAMESPACE+'Identity':
                uri = node.attrib["uri"]
            elif node.tag == ADDON_NAMESPACE+'FriendlyName':
                name = node.attrib["name"]
                version = node.attrib.get("version")
            elif node.tag == ADDON_NAMESPACE+'Icon':
                icon = node.attrib["path"]
            elif node.tag == ADDON_NAMESPACE+'Metamodel':
                path = ''
                for info in node:
                    if node.tag == ADDON_NAMESPACE+'Path':
                        path = node.attrib["icon"]
                component = CMetamodelAddonComponent(path)
        
        return CAddon(storage, uri, component, name, version, icon)
    
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
        l.sort(key = lambda x: x.GetName())
        for addon in l:
            yield addon
