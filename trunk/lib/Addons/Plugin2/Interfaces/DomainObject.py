from ..PluginBase import params, mainthread, polymorphic

from lib.Commands.Properties import CSetPropertyValuesCommand, CAppendPropertyItemCommand, CRemovePropertyItemCommand
from lib.Domains import CDomainObject
from lib.consts import LENGTH_PROPERTY

class IDomainObject(object):
    def __init__(self, plugin, object):
        self.__plugin = plugin
        self.__object = object
    
    @params(str)
    def GetValue(self, path):
        res = self.__object.GetValue(path)
        if isinstance(res, CDomainObject):
            # TODO: error
            return str(res.GetSaveInfo())
        elif isinstance(res, list):
            # TODO: error
            return '[' + ','.join(str(i.GetSaveInfo()) for i in res) + ']'
        else:
            # TODO: remove str
            return str(res)
    
    @params(str, None)
    def SetValue(self, path, value):
        cmd = CSetPropertyValuesCommand(self.__object, {path: value})
        self.__plugin.GetPluginManager().Execute(cmd)
    
    def GetAllValues(self):
        def encode(prefix, value):
            if isinstance(value, (str, unicode)):
                yield (prefix, unicode(value))
            elif isinstance(value, dict):
                for k, v in value.iteritems():
                    for i in encode(prefix + k, v):
                        yield i
            elif isinstance(value, list):
                yield (prefix + '.' + LENGTH_PROPERTY, len(value))
                for i, v in enumerate(value):
                    for j in encode(prefix + '[' + str(i) + '].', v):
                        yield j
        
        for i in encode('', self.__object.GetSaveInfo()):
            yield i
    
    @params(str)
    def AppendItem(self, path):
        cmd = CAppendPropertyItemCommand(self.__object, path)
        self.__plugin.GetPluginManager().Execute(cmd)
    
    @params(str)
    def RemoveItem(self, path):
        cmd = CRemovePropertyItemCommand(self.__object, path)
        self.__plugin.GetPluginManager().Execute(cmd)
