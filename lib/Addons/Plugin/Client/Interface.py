from lib.Addons.Plugin.Client import classes
from lib.Addons.Plugin.Client.Mainloop import CEmpty, CGtk
from lib.Addons.Plugin.Communication.Connection import CConnection
from Transaction import CTransaction
from lib.Exceptions import *
from lib.Addons.Plugin.Communication.Encoding import *

class CInterface(object):
    
    def __init__(self, port):
        self.mainloop = CEmpty()
        self.inmainloop = False
        self.connection = CConnection(port, self.mainloop)
        self.adapter = classes['IAdapter']('#adapter', self.connection)
    
    def _Init(self, uri):
        return self.connection.Execute('plugin', 'init', (), {'uri': EncodeValue(uri, False, self.connection)})()
        
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
    
    def GetAdapter(self):
        return self.adapter
    
    def StartAutocommit(self):
        return self.connection.Execute('transaction', 'autocommit', (), {})()
    
    def BeginTransaction(self):
        return self.connection.Execute('transaction', 'begin', (), {})()
    
    def CommitTransaction(self):
        return self.connection.Execute('transaction', 'commit', (), {})()
        
    def RollbackTransaction(self):
        return self.connection.Execute('transaction', 'rollback', (), {})()
    
    def GetTransaction(self):
        return CTransaction(self)
