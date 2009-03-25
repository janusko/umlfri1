from lib.Plugin.Communication.ComSpec import *

def param(name, test):
    def _param(fun):
        if hasattr(fun, '_params'):
            fun._params[name] = test
        else:
            fun._params = {name: test}
        return fun
    return _param

class CMetamodel(object):
    
    def __init__(self, manager, app):
        self.app = app
        self.manager = manager
    
    def execute(self, ctype, params):
        try:
            fun = getattr(self, ctype)
    
    def GetID(self):
        pass
    
    def ElementList(self):
        pass
    
    def ConnectionList(self):
        pass
    
    def DiagramList(self):
        pass
    
    def DomainList(self):
        pass
    
    def ElementDetail(self, name):
        pass
    
    def 
    
    
    