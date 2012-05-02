from lib.Addons.Plugin.Client import classes
from lib.Addons.Plugin.Client.Mainloop import CEmpty, CGtk
from lib.Addons.Plugin.Communication.Connection import CConnection
from Transaction import CTransaction
from lib.Exceptions import *
from lib.Addons.Plugin.Communication.Encoding import *

class CInterface(object):
    
    def __init__(self, sock):
        self.mainloop = CEmpty()
        self.inmainloop = False
        self.connection = CConnection(sock, self.mainloop)
        self.adapter = classes['IAdapter']('#adapter', self.connection)
        self.stopaction = None
    
    def _Connect(self, uri):
        return self.connection.Execute('plugin', 'connect', (), {'uri': EncodeValue(uri, False, self.connection)})()
    
    def _Initialized(self):
        return self.connection.Execute('plugin', 'initialized', (), {})()
        
    def SetMainloop(self, mainloop):
        if self.inmainloop:
            raise PluginInMainloop('Mainloop object cannot be changed when another one already started')
        self.mainloop = mainloop
        self.connection.SetMainloop(mainloop)
    
    def SetGtkMainloop(self):
        self.SetMainloop(CGtk())
    
    def Mainloop(self):
        self.inmainloop = True
        self.mainloop.Mainloop()
        self.inmainloop = False
        if callable(self.stopaction): 
            self.stopaction()
    
    def GetAdapter(self):
        return self.adapter
        
    def SetStopAction(self, action):
        self.stopaction = action
    
    def PleaseDontKillMe(self, value = True):
        self.connection.Execute('plugin', 'longrun', (), {'value': EncodeValue(bool(value), False, self.connection)})()
