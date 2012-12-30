from Communication.SocketWrapper import CSocketWrapper
from Interface.Core import CCore
from Interface.Transaction import CTransaction
from Interface.Classes.base import IBase
from lib.consts import *
from Watchdog import CWatchdog
import thread, threading, time

class CPluginManager(object):
    '''
    Class that provides management for plugins, their connections
    
    There should be only one instance of this class in application
    '''

    def __init__(self, pluginAdapter):
        IBase.SetAdapter(pluginAdapter)
        self.pluginlock = thread.allocate()
        self.plugins = {}
        self.conlock = thread.allocate()
        self.connection = {}
        self.transaction = {}
        self.addr2uri = {}
        self.accepting = True
        self.pluginAdapter = pluginAdapter
        pluginAdapter._SetPluginManager(self)
        self.proxy = CCore(self, pluginAdapter)
        self.watchdog = CWatchdog(self)
    
    def NewConnection(self, sock, addr):
        '''
        callback from acceptserver
        
        @param sock: connected socket from plugin
        @param addr: identifier of connection
        '''
        if self.accepting:
            with self.conlock:
                self.transaction[addr] = CTransaction(self, addr)
                self.connection[addr] = CSocketWrapper(sock, self.proxy, addr, True)
        else:
            sock.Close()
    
    def AddPlugin(self, plugin):
        with self.pluginlock:
            uri = plugin.GetUri()
            if uri in self.plugins:
                raise Exception() # TODO: replace with better exception
            self.plugins[uri] = plugin
            plugin._SetPluginManager(self)
    
    def ConnectPlugin(self, uri, addr):
        with self.pluginlock:
            if self.plugins[uri].IsInitialized():
                raise Exception() # TODO: replace with better exception
            
            self.addr2uri[addr] = uri
            self.plugins[uri]._Connect(addr)
    
    def PluginSignalInitialized(self, addr):
        uri = self.Addr2Uri(addr)
        if uri in self.plugins:
            plugin = self.plugins[uri]
            plugin._SignalInitialized()
    
    def GetPlugin(self, addr):
        uri = self.Addr2Uri(addr)
        if uri in self.plugins:
            return self.plugins[uri]
        else:
            return None
    
    def GetGuiManager(self):
        '''
        @return: GuiManager instance
        '''
        return self.pluginAdapter.GetGuiManager()
    
    def GetPluginAdapter(self):
        return self.pluginAdapter
    
    def Send(self, addr, code, **params):
        with self.conlock:
            if addr not in self.connection:
                return
            if self.connection[addr].Opened():
                self.connection[addr].Send(code, '', params)
            else:
                del self.connection[addr]
            
    
    def SendToAll(self, code, **params):
        with self.conlock:
            for addr in self.connection.keys(): #this must use list, not iterator (beware in python 3.x)
                self.Send(addr, code, **params)
            
    def GetPort(self):
        if PLUGIN_SOCKET is not None:
            return self.acceptserver.GetPort()
        else:
            return None
    
    def GetTransaction(self, addr):
        return self.transaction[addr]
    
    def GetPluginList(self):
        with self.pluginlock:
            return list(self.plugins.itervalues()) 
        #this is required to return list because it is used 
        # for iteration and is likely to change
    
    def RemovePlugin(self, plugin):
        plugin.IsAlive()
        self.__removePlugin(plugin.GetUri(), plugin.GetAddr())
    
    def __removePlugin(self, uri, addr):
        with self.pluginlock:
            with self.conlock:
                plugin = self.plugins.get(uri, None)
                if plugin is not None:
                    if plugin.IsAlive() and not plugin.GetLongRun():
                        threading.Thread(None, self.KillTask, None, (plugin, )).start()
                    self.plugins[uri]._Disconnect()
                if addr in self.connection:
                    self.connection[addr].Close()
                    del self.connection[addr]
    
    def RemoveByAddr(self, addr):
        self.__removePlugin(self.addr2uri.get(addr, None), addr)
        self.GetGuiManager().DisposeOf(addr)
        
    def Stop(self):
        self.accepting = False
        self.watchdog.Stop()
        if PLUGIN_SOCKET is not None:
            self.acceptserver.Stop()
        for plugin in list(self.plugins.itervalues()):
            if plugin.IsAlive() and not plugin.GetLongRun():
                threading.Thread(None, self.KillTask, None, (plugin, )).start()
    
    def Addr2Uri(self, addr):
        return self.addr2uri.get(addr, None)
            
    def SetLongRun(self, value, addr):
        with self.conlock:
            with self.pluginlock:
                uri = self.Addr2Uri(addr)
                if uri in self.plugins:
                    plugin = self.plugins[uri]
                    plugin.SetLongRun(value)
                    
    def KillTask(self, plugin):
        for i in xrange(10):
            if plugin.IsAlive():
                time.sleep(.05)
            else:
                return
        plugin.Terminate()
        for i in xrange(5):
            if plugin.IsAlive():
                time.sleep(.05)
            else:
                return 
        plugin.Kill()
