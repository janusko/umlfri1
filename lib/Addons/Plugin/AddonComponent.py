import os.path
import sys
import platform

from Plugin import CPlugin
from Starter import starters
from PatchPlugin import CPatchPlugin

class CPluginAddonComponent(object):
    def __init__(self, codes, patches, requiredMetamodels, patchParams):
        self.__allowedOs = ('all', platform.system(), platform.system() + ' ' + platform.version())
        self.__path = None
        self.__starter = None
        self.__codes = codes
        
        self.__patchPaths = patches
        self.__patches = None
        self.__requiredMetamodels = requiredMetamodels
        self.__plugin = None
        self.__metamodel = None
        
        self.__patchParams = patchParams
        self.__patchStarted = True
    
    def _SetAddon(self, addon):
        self.__addon = addon
    
    def GetType(self):
        return 'plugin'
    
    def Start(self):
        if self.__patches is None:
            self.__patches = []
            
            root = self.__addon.GetStorage().get_path()
            
            for path in self.__patchPaths:
                self.__patches.append(CPatchPlugin(self.__patchParams, self.__addon.GetDefaultUri(), root, path))
        
        for patch in self.__patches:
            patch.Start()
            self.__patchStarted = True
        
        if self.__plugin is None:
            path, starter = self.GetStarter()
            if path is not None:
                self.__plugin = CPlugin(os.path.join(root, self.__path), self.__addon.GetDefaultUri(), starter)
                self.__addon.GetManager().GetPluginManager().AddPlugin(self.__plugin)
        
        if self.__path is not None:
            self.__plugin.Start()
    
    def Stop(self):
        if self.__plugin is not None:
            self.__plugin.Stop()
        
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
                self.__patchStarted = False
    
    def Terminate(self):
        if self.__plugin is not None:
            self.__plugin.Terminate()
            
    def Kill(self):
        if self.__plugin is not None:
            self.__plugin.Kill()
            
    def IsRunning(self):
        if self.__plugin is not None:
            return self.__plugin.IsAlive()
        else:
            return self.__patchStarted
    
    def GetStarter(self):
        if self.__starter is None:
            for osName, language, path in self.__codes:
                if osName in self.__allowedOs:
                    self.__starter = starters[language]
                    self.__path = path
                    break
        return self.__path, self.__starter
