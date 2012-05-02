import uuid
import os
import weakref

from Communication.ComSpec import *

from lib.config import config

class CPlugin(object):
    def __init__(self, path, uri, starter):
        self.__uri = uri
        self.__path = path
        self.__pluginManager = None
        self.__addr = None
        self.__starter = starter(self)
    
    def GetUri(self):
        return self.__uri
    
    def GetPath(self):
        return self.__path
    
    def GetPluginManager(self):
        return self.__pluginManager()
    
    def IsInitialized(self):
        return self.__addr is not None
    
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
    
    def Poll(self):
        return self.__starter.Poll()
        
    def IsAlive(self):
        return self.Poll() is None
    
    def _SetPluginManager(self, manager):
        self.__pluginManager = weakref.ref(manager)
    
    def _Connect(self, addr):
        self.__addr = addr
