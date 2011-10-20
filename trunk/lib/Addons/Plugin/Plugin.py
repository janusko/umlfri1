import uuid
import os
import weakref

from Communication.ComSpec import *

from lib.config import config

class CPlugin(object):
    def __init__(self, path, uri, starter, addon):
        self.__uri = uri
        self.__path = path
        self.__pluginManager = None
        self.__addr = None
        self.__starter = starter(self)
        self.__longrun = False
        self.__initialized = False
        self.__addon = addon
    
    def GetUri(self):
        return self.__uri
    
    def GetAddon(self):
        return self.__addon
    
    def GetPath(self):
        return self.__path
    
    def GetPluginManager(self):
        return self.__pluginManager()
    
    def IsInitialized(self):
        return self.__addr is not None and self.__initialized
    
    def Start(self):
        self.__starter.Start()
    
    def Stop(self):
        if self.IsInitialized():
            self.__pluginManager().Send(self.__addr, RESP_FINALIZE)
    
    def ClearGui(self):
        self.__pluginManager().GetGuiManager().DisposeOf(self.__addr)
    
    def Terminate(self):
        self.__starter.Terminate()
        
    def Kill(self):
        self.__starter.Kill()
    
    def IsAlive(self):
        return self.__starter.IsAlive()
    
    def _SetPluginManager(self, manager):
        self.__pluginManager = weakref.ref(manager)
    
    def _Connect(self, addr):
        self.__addr = addr
    
    def _SignalInitialized(self):
        self.__initialized = True
    
    def _Disconnect(self):
        self.__addr = None
        self.__initialized = False
    
    def GetAddr(self):
        return self.__addr
        
    def Dispose(self):
        self.ClearGui()
        self.__pluginManager().RemovePlugin(self)
        self.__initialized = False
        
    def GetPid(self):
        return self.__starter.GetPid()
    
    def SetLongRun(self, value):
        self.__longrun = value
    
    def GetLongRun(self):
        return self.__longrun
