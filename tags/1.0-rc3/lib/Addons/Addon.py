class CAddon(object):
    def __init__(self, manager, storage, uris, component, enabled, uninstallable,
                    author, name, version = "", license = (None, None), homepage = None,
                    icon = None, description = None):
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
        self.__version = version
        
        self.__icon = icon
        self.__description = description
    
    def GetStorage(self):
        return self.__storage
    
    def GetDefaultUri(self):
        return self.__uris[0]
    
    def GetUris(self):
        for uri in self.__uris:
            yield uri
    
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
    
    def Stop(self):
        self.__component.Stop()
    
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
