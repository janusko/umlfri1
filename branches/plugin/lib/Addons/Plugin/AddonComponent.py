import os.path
import platform

from Plugin import CPlugin

class CPluginAddonComponent(object):
    def __init__(self, codes, requiredMetamodels):
        allowedOs = ('all', platform.system(), platform.system() + ' ' + platform.version())
        self.__path = None
        
        for osName, language, path in codes:
            if osName in allowedOs and language == 'python':
                self.__path = path
                break
        
        self.__requiredMetamodels = requiredMetamodels
        self.__plugin = None
        self.__metamodel = None
    
    def _SetAddon(self, addon):
        self.__addon = addon
    
    def GetType(self):
        return 'plugin'
    
    def Start(self):
        if self.__path is None:
            return
        
        if self.__plugin is None:
            self.__plugin = CPlugin(os.path.join(self.__addon.GetStorage().get_path(), self.__path), self.__addon.GetDefaultUri())
            self.__addon.GetManager().GetPluginManager().AddPlugin(self.__plugin)
        
        self.__plugin.Start()
    
    def Stop(self):
        if self.__plugin is None:
            return
        
        self.__plugin.Stop()
