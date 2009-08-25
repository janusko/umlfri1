import uuid
import os
import weakref

from Communication.ComSpec import *

from lib.config import config

class CPlugin(object):
    def __init__(self, path, uri):
        self.__uri = uri
        self.__path = path
        self.__pluginManager = None
        self.__password = str(uuid.uuid1())
        self.__addr = None
    
    def GetUri(self):
        return self.__uri
    
    def IsInitialized(self):
        return self.__addr is not None
    
    def Start(self):
        if os.path == 'nt': 
            os.system('start /B pl_runner.py %i "%s" "%s" "%s"' % (self.__pluginManager().GetPort(), self.__path, self.__uri, self.__password))
        else:
            os.system(config['/Paths/Root'] + 'pl_runner.py %i "%s" "%s" "%s" &' % (self.__pluginManager().GetPort(), self.__path, self.__uri, self.__password))
    
    def Stop(self):
        if self.IsInitialized():
            self.__pluginManager().Send(self.__addr, RESP_FINALIZE)
    
    def _SetPluginManager(self, manager):
        self.__pluginManager = weakref.ref(manager)
    
    def _VerifyPassword(self, password):
        return self.__password == password
    
    def _Connect(self, addr):
        self.__addr = addr
