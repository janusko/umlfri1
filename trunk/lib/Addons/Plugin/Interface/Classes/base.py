from lib.Addons.Plugin.Interface.meta import Meta
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import r_str
import os, os.path

class IBase(object):
    __metaclass__ = Meta
    __cls__ = None
    adapter = None
    
    @classmethod
    @not_interface
    def SetAdapter(cls, adapter):
        cls.adapter = adapter
        
    @classmethod
    @not_interface
    def GetAdapter(cls):
        return cls.adapter
        
    @classmethod
    @not_interface
    def GetStorage(cls, addr):
        try:
            uri = IBase.adapter.GetPluginManager().Addr2Uri(addr)
            app = IBase.adapter.GetApplication()
            addonMgr = app.GetAddonManager()
            addon = addonMgr.GetAddon(uri)
            storage = addon.GetStorage()
            return storage
        except AttributeError:
            return None
    
    @classmethod
    @not_interface
    def RelativePath2Absolute(cls, addr, path):
        storage = cls.GetStorage(addr)
        if storage is not None:
            return os.path.join(storage.get_path(), path)
        else:
            return None
        
    
    
