from lib.Addons.AddonStarter import CAddonStarter
from lib.Addons.AddonStopper import CAddonStopper
from lib.datatypes import CVersion

class CAddon(object):
    def __init__(self, manager, storage, uris, component, enabled, uninstallable,
                    author, name, version, license = (None, None), homepage = None,
                    icon = None, description = None,
                    umlfriVersionRange = None, dependencies = [],
                    updateUrl = None):
        self.__manager = manager
        
        self.__storage = storage
        self.__uris = uris
        
        self.__component = component
        component._SetAddon(self)
        
        self.__enabled = enabled
        self.__uninstallable = uninstallable
        
        self.__author = author
        self.__license = license
        self.__homepage = homepage
        
        self.__name = name
        self.__version = CVersion(version)
        
        self.__icon = icon
        self.__description = description
        
        self.__umlfriVersionRange = umlfriVersionRange
        self.__dependencies = dependencies
        
        self.__updateUrl = updateUrl
    
    def GetStorage(self):
        return self.__storage
    
    def GetDefaultUri(self):
        return self.__uris[0]
    
    def GetUris(self):
        for uri in self.__uris:
            yield uri
    
    def GetUpdateUrl(self):
        return self.__updateUrl
    
    def IsEnabled(self):
        return self.__enabled
    
    def Enable(self):
        self.__enabled = True
        self.__manager._RefreshAddonEnabled(self)
    
    def Disable(self):
        self.__enabled = False
        self.__manager._RefreshAddonEnabled(self)
    
    def Start(self):
        self.__component.Start()
    
    def StartWithDeps(self):
        return CAddonStarter(self.__manager, [self])
    
    def Stop(self):
        self.__component.Stop()
    
    def StopWithDeps(self):
        return CAddonStopper(self.__manager, [self])
        
    def Terminate(self):
        self.Disable()
        self.__component.Terminate()
    
    def Kill(self):
        self.Disable()
        self.__component.Kill()
    
    def GetRunInProcess(self):
        return self.__component.GetRunInProcess()
        
    def IsRunning(self):
        return self.__component.IsRunning()
    
    def GetAuthor(self):
        return self.__author
    
    def GetLicense(self):
        return self.__license[1]
    
    def GetLicenseName(self):
        return self.__license[0]
    
    def GetHomepage(self):
        return self.__homepage
    
    def GetName(self):
        return self.__name
    
    def GetVersion(self):
        return self.__version
    
    def GetVersionString(self):
        return str(self.__version)
    
    def GetComponent(self):
        return self.__component
    
    def GetType(self):
        return self.__component.GetType()
    
    def GetIcon(self):
        return self.__icon
    
    def GetDescription(self):
        return self.__description
    
    def IsUninstallable(self):
        return self.__uninstallable
    
    def Uninstall(self):
        self.__storage.destroy()
        self.__manager._DeleteAddon(self)
    
    def GetManager(self):
        return self.__manager
    
    def GetDependencies(self):
        for dep in self.__dependencies:
            yield dep
                
    def CheckUmlFriDependencies(self):
        if self.__umlfriVersionRange is not None:
            ver = self.__manager.GetPluginManager().GetPluginAdapter().GetUmlfriVersion()
            verFrom, verTo = self.__umlfriVersionRange
            
            if verFrom is not None and ver < verFrom:
                return False
            if verTo is not None and ver > verTo:
                return False
        return True
