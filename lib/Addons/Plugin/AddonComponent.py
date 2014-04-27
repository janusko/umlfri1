from .PatchPlugin import CPatchPlugin
from .Implementation.Plugin import CPlugin
from .Starter import STARTERS

import platform
import os.path

class CPluginAddonComponent(object):
    __allowedOs = ('all', platform.system(), platform.system() + ' ' + platform.version())
    
    def __init__(self, codes, patches, patchParams):
        self.__codes = codes
        
        self.__addon = None
        
        self.__patchPaths = patches
        self.__patchParams = patchParams
        self.__patches = None
        self.__patchStarted = False
        
        self.__plugin = None
        self.__starter = None
        self.__path = None
    
    def _SetAddon(self, addon):
        self.__addon = addon
    
    def GetType(self):
        return 'plugin'
    
    def Start(self):
        root = self.__addon.GetStorage().get_path()
        
        if self.__patches is None:
            self.__patches = []
            
            for path in self.__patchPaths:
                self.__patches.append(CPatchPlugin(self.__patchParams, self.__addon.GetDefaultUri(), root, path))
        
        for patch in self.__patches:
            patch.Start()
            self.__patchStarted = True
        
        path, starter = self.__GetStarter()
        if path is not None:
            channel = starter.Start()
            self.__plugin = CPlugin(channel, self.__path, self.__addon.GetManager().GetPluginAdapter())
    
    def Stop(self):
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
            self.__patchStarted = False
        
        if self.__plugin is not None:
            self.__plugin.SendStop()
    
    def Terminate(self):
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
            self.__patchStarted = False
        
        if self.__plugin is not None:
            self.__starter.Terminate()
        
    def Kill(self):
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
            self.__patchStarted = False
        
        if self.__plugin is not None:
            self.__starter.Kill()
        
    def IsRunning(self):
        return self.__patchStarted or (self.__starter is not None and self.__starter.IsAlive())
    
    def GetRunInProcess(self):
        return self.__codes is not None
    
    def GetUri(self):
        return self.__addon.GetDefaultUri()
    
    def GetPath(self):
        return self.__path
    
    def __GetStarter(self):
        root = self.__addon.GetStorage().get_path()
        
        if self.__codes is not None:
            if self.__starter is None:
                for osName, language, path in self.__codes:
                    if osName in self.__allowedOs:
                        self.__starter = STARTERS[language](self)
                        self.__path = os.path.join(root, path)
                        break
        return self.__path, self.__starter
