from lib.Addons.AddonStarter import CAddonStarter
from lib.Depend.libxml import etree

import re
import os
import os.path
import uuid

from lib.lib import Indent
from lib.Storages import open_storage, CDirectory
from Addon import CAddon
from Dependency import CDependency
from lib.datatypes import CVersion

from Composite.AddonComponent import CCompositeAddonComponent
from Metamodel.AddonComponent import CMetamodelAddonComponent
from Plugin.AddonComponent import CPluginAddonComponent
from Plugin.Manager import CPluginManager
from lib.consts import ADDON_NAMESPACE, ADDON_LIST_NAMESPACE
from lib.Distconfig import SCHEMA_PATH, USERDIR_PATH, ADDONS_PATH
from lib.config import config
from lib.Exceptions.DevException import *
from lib.Update.UpdateManager import CUpdateManager as CUpdateManager
from lib.Update.UpdateRequest import CUpdateRequest as CUpdateRequest

xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "addon.xsd"))
xmlschema = etree.XMLSchema(xmlschema_doc)
xmlschema_list_doc = etree.parse(os.path.join(SCHEMA_PATH, "addonList.xsd"))
xmlschema_list = etree.XMLSchema(xmlschema_list_doc)

class CAddonManager(object):
    reSpaces = re.compile(' +')
    reIlegalCharacters = re.compile('[^a-z0-9A-Z]')
    
    def __init__(self, pluginAdapter, patchParams):
        self.__patchParams = patchParams
        
        self.__enabledAddons = self.__LoadEnabledAddons(os.path.join(USERDIR_PATH, 'addons.xml'))
        self.__addons = self.__LoadAllAddons(open_storage(ADDONS_PATH), False)
        self.__addons.update(self.__LoadAllAddons(open_storage(os.path.join(USERDIR_PATH, 'addons')), True))
        self.__pluginManager = CPluginManager(pluginAdapter)
        self.__updateManager = CUpdateManager()
    
    def __LoadEnabledAddons(self, path):
        ret = {}
        
        if not os.path.exists(path):
            return ret
        
        root = etree.XML(file(path).read())
        if not xmlschema_list.validate(root):
            raise FactoryError("XMLError", xmlschema_list.error_log.last_error)
        
        for node in root:
            ret[node.attrib['uri']] = node.attrib.get('enabled', 'true').lower() in ('true', 'yes', '1')
        
        return ret
    
    def __SaveEnabledAddons(self, path, values):
        root = etree.XML("<AddOns xmlns=\"%s\"/>"%ADDON_LIST_NAMESPACE[1:-1])
        
        for uri, enabled in values.iteritems():
            root.append(etree.Element(ADDON_LIST_NAMESPACE+"AddOn", uri = uri, enabled = str(int(enabled))))
        
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
        tmp = self.__AddAddonToDict(self.__LoadAddon(storage, uninstallable))
        
        return tmp
    
    def __AddAddonToDict(self, addon):
        tmp = {}
        
        if addon is not None:
            for uri in addon.GetUris():
                tmp[uri] = addon
        
        return tmp
    
    def __LoadAddon(self, storage, uninstallable):
        if storage is None:
            return None
        
        if not storage.exists('addon.xml'):
            return None
        
        root = etree.XML(storage.read_file('addon.xml'))
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
        umlfriVersionRange = None
        dependencies = []
        updateUrl = None
        
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
                description = self.__FormatMultilineText(node.text or '')
            elif node.tag == ADDON_NAMESPACE+'Updates':
                updateUrl = node.attrib["url"]
            elif node.tag == ADDON_NAMESPACE+'Dependencies':
                umlfriVersionRange, dependencies = self.__LoadDependencies(node)
            elif node.tag == ADDON_NAMESPACE+'Metamodel':
                component = self.__LoadMetamodelAddonComponent(node)
            elif node.tag == ADDON_NAMESPACE+'Plugin':
                component = self.__LoadPluginAddonComponent(node)
            elif node.tag == ADDON_NAMESPACE+'Composite':
                component = self.__LoadCompositeAddonComponent(node)
        
        return CAddon(self, storage, uris, component,
            False,
            uninstallable, author, name, version, license, homepage,
            icon, description, umlfriVersionRange, dependencies, updateUrl)
    
    def __LoadDependencies(self, node):
        umlfriVersionRange = None
        dependencies = []
        
        for child in node:
            if child.tag == ADDON_NAMESPACE+'UmlFri':
                umlfriVersionRange = self.__LoadDepVersionInfo(child)
            elif child.tag == ADDON_NAMESPACE+'AddOn':
                dependencies.append(
                    CDependency(
                        child.attrib['uri'],
                        required = node.attrib.get('required', 'true').lower() in ('true', 'yes', '1'),
                        versionRange = self.__LoadDepVersionInfo(child)
                    )
                )
        
        return umlfriVersionRange, dependencies
    
    def __LoadDepVersionInfo(self, node):
        for child in node:
            if child.tag == ADDON_NAMESPACE+'Version':
                verFrom = child.attrib.get('min')
                verTo = child.attrib.get('max')
                
                if verFrom is not None:
                    verFrom = CVersion(verFrom)
                if verTo is not None:
                    verTo = CVersion(verTo)
                
                return verFrom, verTo
        
        return None
    
    def __LoadMetamodelAddonComponent(self, node):
        path = ''
        templates = []
        for info in node:
            if info.tag == ADDON_NAMESPACE+'Path':
                path = info.attrib["path"]
            if info.tag == ADDON_NAMESPACE+'Template':
                templates.append((info.attrib.get("name"), info.attrib.get("icon"), info.attrib.get("path")))
        
        return CMetamodelAddonComponent(path, templates)
    
    def __LoadPluginAddonComponent(self, node):
        codes = []
        requiredMetamodels = []
        patches = []
        
        for info in node:
            if info.tag == ADDON_NAMESPACE+'Code':
                codes.append((info.get("os", "all"), info.attrib["language"], info.attrib["path"]))
            elif info.tag == ADDON_NAMESPACE+'Patch':
                patches.append(info.attrib["module"])
            elif info.tag == ADDON_NAMESPACE+'Metamodel':
                requiredMetamodels.append(info.attrib["required"])
        
        return CPluginAddonComponent(codes, patches, requiredMetamodels, self.__patchParams)
    
    def __LoadCompositeAddonComponent(self, node):
        components = {}
        
        for info in node:
            if info.tag == ADDON_NAMESPACE+'Metamodel':
                components['metamodel'] = self.__LoadMetamodelAddonComponent(info)
            elif info.tag == ADDON_NAMESPACE+'Plugin':
                components['plugin'] = self.__LoadPluginAddonComponent(info)
        
        return CCompositeAddonComponent(**components)
    
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
    
    def GetPluginManager(self):
        return self.__pluginManager
    
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
    
    def ListEnabledAddons(self, type = None):
        for addon in self.ListAddons(type):
            if addon.IsEnabled():
                yield addon
    
    def Save(self):
        self.__SaveEnabledAddons(os.path.join(USERDIR_PATH, 'addons.xml'), self.__enabledAddons)
    
    def LoadAddon(self, storage):
        if isinstance(storage, (str, unicode)):
            storage = open_storage(storage)
        return self.__LoadAddon(storage, False)
    
    def InstallAddon(self, addon):
        dirname = str(uuid.uuid5(uuid.NAMESPACE_URL, addon.GetDefaultUri()))
        path = os.path.join(USERDIR_PATH, 'addons', dirname)
        storage = CDirectory.duplicate(addon.GetStorage(), path)
        
        addon = self.__LoadAddon(storage, True)
        addon.Start()
        self.__addons.update(self.__AddAddonToDict(addon))
    
    def StartAll(self):
        toStart = set(addon for uri, addon in self.__addons.iteritems() if self.__enabledAddons.get(uri, True))
        return CAddonStarter(self, toStart)
    
    def StopAll(self):
        for addon in self.__addons.itervalues():
            if addon.IsRunning():
                addon.Stop()
        self.__pluginManager.Stop()
    
    def CheckAddonUpdates(self):
        """
        Check for installed addon updates. No dependency checking for now.
        
        @return: Old and new addon description
        @rtype: iterator over tuple of L{CAddon<Addon.CAddon>}
        """
        toUpdates = []
        for addon in self.__addons.itervalues():
            url = addon.GetUpdateUrl()
            if url is not None:
                toUpdates.append(CUpdateRequest(url, addon.GetDefaultUri(), addon.GetVersion()))                
        
        updated = self.__updateManager.Update(toUpdates)
        
        for upd in updated:
            storage = open_storage(upd.GetAddon())
            
            if storage is None:
                # TODO: log update error
                continue
            
            try:
                newAddon = self.__LoadAddon(storage, False)
            except:
                # TODO: log update error
                continue
            
            oldAddon = self.GetAddon(upd.GetUri())
            
            if oldAddon is None:
                # TODO: log update error
                continue
            
            if oldAddon.GetVersion() >= newAddon.GetVersion():
                continue
            
            yield oldAddon, newAddon
