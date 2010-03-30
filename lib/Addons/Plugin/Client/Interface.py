from lib.Addons.Plugin.Client import classes
from lib.Addons.Plugin.Client.Mainloop import CEmpty, CGtk
from lib.Addons.Plugin.Communication.Connection import CConnection
from Transaction import CTransaction
from lib.Exceptions import *

class CInterface(object):
    
    def __init__(self, port):
        self.mainloop = CEmpty()
        self.inmainloop = False
        self.connection = CConnection(port, self.mainloop)
        self.adapter = classes['IAdapter']('#adapter', self.connection)
    
    def _Init(self, uri):
        return self.connection.Execute('plugin', 'init', {'uri': uri})()
        
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
    
    def AddMenu(self, mtype, path, name, callback, **params):
        if callback is not None:
            self.connection.SetGuiCallback(path + '/' + name, callback)
        params['type'] = mtype
        params['path'] = path
        params['name'] = name
        return self.connection.Execute('gui', 'add', params)()
    
    def DisplayWarning(self, text):
        return self.connection.Execute('gui', 'warning', {'text': text})()
    
    def StartAutocommit(self):
        return self.connection.Execute('transaction', 'autocommit', {})()
    
    def BeginTransaction(self):
        return self.connection.Execute('transaction', 'begin', {})()
    
    def CommitTransaction(self):
        return self.connection.Execute('transaction', 'commit', {})()
        
    def RollbackTransaction(self):
        return self.connection.Execute('transaction', 'rollback', {})()
    
    def GetTransaction(self):
        return CTransaction(self)
