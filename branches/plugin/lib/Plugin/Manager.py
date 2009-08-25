from Communication.AcceptServer import CAcceptServer
from Communication.SocketWrapper import CSocketWrapper
from Communication.ComSpec import *
from Interface.Core import CCore
from Interface.Transaction import CTransaction
from lib.consts import *
from lib.Gui import CGuiManager
import thread

class CPluginManager(object):
    '''
    Class that provides management for plugins, their connections
    
    There should be only one instance of this class in application
    '''

    def __init__(self, app):
        self.__plugins = {}
        self.conlock = thread.allocate()
        self.connection = {}
        self.transaction = {}
        self.app = app
        self.guimanager = CGuiManager(app)
        self.proxy = CCore(self, app)
        self.acceptserver = CAcceptServer(('localhost', PLUGIN_SOCKET), self.NewConnection)
        self.acceptserver.Start()
        print "PORT:", self.acceptserver.sock.getsockname()[1]
    
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
            #print self.transaction.keys()
        finally:
            self.conlock.release()
    
    def AddPlugin(self, plugin):
        if plugin.GetUri() in self.__plugins:
            raise Exception() # TODO: replace with better exception
        self.__plugins[plugin.GetUri()] = plugin
        plugin._SetPluginManager(self)
    
    def ConnectPlugin(self, uri, password, addr):
        if self.__plugins[uri].IsInitialized():
            raise Exception() # TODO: replace with better exception
        
        if not self.__plugins[uri]._VerifyPassword(password):
            raise Exception() # TODO: replace with better exception
        
        self.__plugins[uri]._Connect(addr)
    
    def GetGuiManager(self):
        '''
        @return: GuiManager instance
        '''
        return self.guimanager
    
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
            
    def DomainValueChanged(self, element, path):
        self.SendToAll(RESP_DOMAIN_VALUE_CHANGED, element = r_object(element), path = path)
    
    def KillAll(self):
        self.SendToAll(RESP_FINALIZE)
        
    def GetPort(self):
        return self.acceptserver.sock.getsockname()[1]
    
    def GetTransaction(self, addr):
        return self.transaction[addr]
    
