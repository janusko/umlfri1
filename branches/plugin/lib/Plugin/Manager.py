from AcceptServer import CAcceptServer
from SocketWrapper import CSocketWrapper
from Proxy import CProxy
from lib.consts import *
from GuiManager import CGuiManager
from ComSpec import *
import thread

class CPluginManager(object):
    '''
    Class that provides management for plugins, their connections
    
    There should be only one instance of this class in application
    '''

    def __init__(self, app):
        self.conlock = thread.allocate()
        self.connection = {}
        self.app = app
        self.guimanager = CGuiManager(app)
        self.proxy = CProxy(self)
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
            self.connection[addr] = CSocketWrapper(sock, self.proxy, addr, True)
        finally:
            self.conlock.release()
    
    def GetGuiManager(self):
        '''
        @return: GuiManager instance
        '''
        return self.guimanager
    
    def Send(self, addr, code, **params):
        self.connection[addr].Send(code, '', params)
    
