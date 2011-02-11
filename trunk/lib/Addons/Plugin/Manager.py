from Communication.AcceptServer import CAcceptServer
from Communication.SocketWrapper import CSocketWrapper
from Communication.ComSpec import *
from Interface.Core import CCore
from Interface.Transaction import CTransaction
from Interface.Classes.base import IBase
from lib.consts import *
import thread

class CPluginManager(object):
    '''
    Class that provides management for plugins, their connections
    
    There should be only one instance of this class in application
    '''

    def __init__(self, pluginAdapter):
        IBase.SetAdapter(pluginAdapter)
        self.plugins = {}
        self.conlock = thread.allocate()
        self.connection = {}
        self.transaction = {}
        self.pluginAdapter = pluginAdapter
        pluginAdapter._SetPluginManager(self)
        self.proxy = CCore(self, pluginAdapter)
        if PLUGIN_SOCKET is not None:
            self.acceptserver = CAcceptServer(('localhost', PLUGIN_SOCKET), self.NewConnection)
            self.acceptserver.Start()
    
    def NewConnection(self, sock, addr):
        '''
        callback from acceptserver
        
        @param sock: connected socket from plugin
        @param addr: identifier of connection
        '''
        try:
            self.conlock.acquire()
            self.transaction[addr] = CTransaction()
            self.connection[addr] = CSocketWrapper(sock, self.proxy, addr, True)
        finally:
            self.conlock.release()
    
    def AddPlugin(self, plugin):
        if plugin.GetUri() in self.plugins:
            raise Exception() # TODO: replace with better exception
        self.plugins[plugin.GetUri()] = plugin
        plugin._SetPluginManager(self)
    
    def ConnectPlugin(self, uri, addr):
        if self.plugins[uri].IsInitialized():
            raise Exception() # TODO: replace with better exception
        
        self.plugins[uri]._Connect(addr)
    
    def GetGuiManager(self):
        '''
        @return: GuiManager instance
        '''
        return self.pluginAdapter.GetGuiManager()
    
    def GetPluginAdapter(self):
        return self.pluginAdapter
    
    def Send(self, addr, code, **params):
        if addr not in self.connection:
            return
        if self.connection[addr].Opened():
            self.connection[addr].Send(code, '', params)
        else:
            del self.connection[addr]
            
    
    def SendToAll(self, code, **params):
        try:
            self.conlock.acquire()
            for addr in self.connection.keys(): #this must use list, not iterator (beware in python 3.x)
                self.Send(addr, code, **params)
        finally:
            self.conlock.release()
            
    def GetPort(self):
        if PLUGIN_SOCKET is not None:
            return self.acceptserver.GetPort()
        else:
            return None
    
    def GetTransaction(self, addr):
        return self.transaction[addr]
    
