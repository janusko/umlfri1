class CPluginAddonComponent(object):
    def __init__(self, codes, patches, requiredMetamodels, patchParams):
        self.__addon = None
    
    def _SetAddon(self, addon):
        self.__addon = addon
    
    def GetType(self):
        return 'plugin'
    
    def Start(self):
        pass
    
    def Stop(self):
        pass
    
    def Terminate(self):
        pass
        
    def Kill(self):
        pass
        
    def IsRunning(self):
        return False
    
    def GetRunInProcess(self):
        return False
