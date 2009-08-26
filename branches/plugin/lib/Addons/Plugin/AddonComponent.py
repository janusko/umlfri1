import os.path
import sys
import platform

from Plugin import CPlugin
from Starter import starters

class CPluginAddonComponent(object):
    def __init__(self, codes, patches, requiredMetamodels):
        allowedOs = ('all', platform.system(), platform.system() + ' ' + platform.version())
        self.__path = None
        self.__starter = None
        
        for osName, language, path in codes:
            if osName in allowedOs and language in starters:
                self.__path = path
                self.__starter = starters[language]
                break
        
        self.__patchPaths = patches
        self.__patches = None
        self.__requiredMetamodels = requiredMetamodels
        self.__plugin = None
        self.__metamodel = None
    
    def _SetAddon(self, addon):
        self.__addon = addon
    
    def GetType(self):
        return 'plugin'
    
    def Start(self):
        if self.__patches is None:
            self.__patches = []
            
            root = self.__addon.GetStorage().get_path()
            
            for path, module in self.__patchPaths:
                path = os.path.abspath(os.path.join(root, path))
                if path not in sys.path:
                    sys.path.append(path)
                self.__patches.append(__import__(module).Plugin(None, None)) # TODO: set to current app and app type
        
        for patch in self.__patches:
            patch.Start()
        
        if self.__path is not None:
            if self.__plugin is None:
                self.__plugin = CPlugin(os.path.join(root, self.__path), self.__addon.GetDefaultUri(), self.__starter)
                self.__addon.GetManager().GetPluginManager().AddPlugin(self.__plugin)
            
            self.__plugin.Start()
    
    def Stop(self):
        if self.__plugin is not None:
            self.__plugin.Stop()
        
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
