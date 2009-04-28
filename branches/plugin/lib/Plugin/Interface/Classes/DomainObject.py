from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *

class IDomainObject(IBase):
    __cls__ = None
    
    def GetName(him):
        return him.GetName()
    
    def GetValue(him, path):
            res = him.GetValue(path)
            if isinstance(res, CDomainObject):
                return `res.GetSaveInfo()`
            elif isinstance(res, list):
                return '[' + ','.join(`i.GetSaveInfo()` for i in res) + ']'
            else:
                return `res`
    
    def SetValue(him, path, value):
        him.SetValue(path, value)
        IBase.adapter.plugin_change_domain_value(him, path)
    
    def GetSaveInfo(him):
        return `him.GetSaveInfo()`
    
    def GetType(him):
        return him.GetType().GetId()

