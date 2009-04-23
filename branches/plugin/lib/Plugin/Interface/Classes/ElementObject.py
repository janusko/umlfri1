from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Domains.Object import CDomainObject
from lib.Exceptions import *

class IElementObject(IBase):
    __cls__ = CElementObject
    
    @parameter('con', t_classobject(CConnectionObject))
    def AddConnection(self, con):
        return self.AddConnection(con)
    
    def GetName(self):
        return self.GetName()
    
    def GetValue(self, path):
        try:
            res = self.GetValue(path)
            if isinstance(res, CDomainObject):
                return `res.GetSaveInfo()`
            elif isinstance(res, list):
                return '[' + ','.join(`i.GetSaveInfo()` for i in res) + ']'
            else:
                return `res`
        except (DomainObjectException,):
            raise 
    
    def GetSaveInfo(self):
        return `self.GetSaveInfo()`
