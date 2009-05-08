from lib.Plugin.Client import classes
from lib.Plugin.Communication.Connection import CConnection

class CInterface(object):
    
    def __init__(self, port):
        self.connection = CConnection(port)
        self.project = classes['IProject']('project', self.connection)
    
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
        return self._metamodel('detail.metamodel', {})
    
    def DetailDiagram(self, name):
        return self._metamodel('detail.diagram', {'name': name})
    
    def DetailElement(self, name):
        return self._metamodel('detail.element', {'name': name})
    
    def DetailConnection(self, name):
        return self._metamodel('detail.connection', {'name': name})
    
    def DetailDomain(self, name):
        return self._metamodel('detail.domain', {'name': name})
    
    def ListElement(self):
        return self._metamodel('list.element')
    
    def ListConnection(self):
        return self._metamodel('list.connection')
    
    def ListDomain(self):
        return self._metamodel('list.domain')
