from lib.Addons.Plugin.Client import classes
from lib.Addons.Plugin.Communication.Connection import CConnection
from Transaction import CTransaction

class CInterface(object):
    
    def __init__(self, port):
        self.connection = CConnection(port)
        self.project = classes['IProject']('project', self.connection)
    
    def _Init(self, uri):
        return self.connection.Execute('plugin', 'init', {'uri': uri})()
    
    def WaitTillClosed(self):
        return self.connection.WaitTillClosed()
    
    def GetProject(self):
        return self.project
        
    def AddMenu(self, mtype, path, name, callback, **params):
        if callback is not None:
            self.connection.SetGuiCallback(path + '/' + name, callback)
        params['type'] = mtype
        params['path'] = path
        params['name'] = name
        return self.connection.Execute('gui', 'add', params)()
    
    def DisplayWarning(self, text):
        return self.connection.Execute('gui', 'warning', {'text': text})()
    
    def _metamodel(self, ctype, params = {}):
        res = self.connection.Execute('metamodel', ctype, params)
        return eval(res(), {}, {'__builtins__': {}})
    
    def DetailMetamodel(self):
        return self._metamodel('metamodel.detail', {})
    
    def DetailDiagram(self, name):
        return self._metamodel('diagram.detail', {'name': name})
    
    def DetailElement(self, name):
        return self._metamodel('element.detail', {'name': name})
    
    def DetailConnection(self, name):
        return self._metamodel('connection.detail', {'name': name})
    
    def DetailDomain(self, name):
        return self._metamodel('domain.detail', {'name': name})
    
    def ListElement(self):
        return self._metamodel('element.list')
    
    def ListConnection(self):
        return self._metamodel('connection.list')
    
    def ListDomain(self):
        return self._metamodel('domain.list')
        
    def ListDiagram(self):
        return self._metamodel('diagram.list')
        
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
