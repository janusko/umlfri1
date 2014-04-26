from .PatchPlugin import CPatchPlugin


class CPluginAddonComponent(object):
    def __init__(self, codes, patches, requiredMetamodels, patchParams):
        self.__addon = None
        self.__patchPaths = patches
        self.__patchParams = patchParams
        self.__patches = None
        self.__patchStarted = False
    
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
    
    def Stop(self):
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
            self.__patchStarted = False
    
    def Terminate(self):
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
            self.__patchStarted = False
        
    def Kill(self):
        if self.__patches is not None:
            for patch in self.__patches:
                patch.Stop()
            self.__patchStarted = False
        
    def IsRunning(self):
        return self.__patchStarted
    
    def GetRunInProcess(self):
        return False
