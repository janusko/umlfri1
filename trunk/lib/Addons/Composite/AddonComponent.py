import weakref
import os.path

class CCompositeAddonComponent(object):
    def __init__(self, metamodel, plugin):
        self.__metamodel = metamodel
        self.__plugin = plugin
    
    def _SetAddon(self, addon):
        self.__metamodel._SetAddon(addon)
        self.__plugin._SetAddon(addon)
    
    def LoadMetamodel(self):
        return self.__metamodel.LoadMetamodel()
    
    def GetTemplates(self):
        return self.__metamodel.GetTemplates()
    
    def GetType(self):
        return 'composite'
    
    def Start(self):
        self.__metamodel.Start()
        self.__plugin.Start()
    
    def Stop(self):
        self.__metamodel.Stop()
        self.__plugin.Stop()
    
    def Terminate(self):
        self.__metamodel.Terminate()
        self.__plugin.Terminate()
        
    def Kill(self):
        self.__metamodel.Kill()
        self.__plugin.Kill()
        
    def IsRunning(self):
        return self.__metamodel.IsRunning() or self.__plugin.IsRunning()
