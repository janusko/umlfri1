from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *

class IDomainObject(IBase):
    __cls__ = None
    
    @result(r_str)
    def GetName(him):
        return him.GetName()
    
    @result(r_str)
    @parameter('path', t_str)
    def GetValue(him, path):
            res = him.GetValue(path)
            if isinstance(res, CDomainObject):
                return `res.GetSaveInfo()`
            elif isinstance(res, list):
                return '[' + ','.join(`i.GetSaveInfo()` for i in res) + ']'
            else:
                return `res`
    
    @result(r_str)
    def GetSaveInfo(him):
        return `him.GetSaveInfo()`
    
    @result(r_str)
    def GetType(him):
        return him.GetType().GetId()
    
    @result(r_objectlist)
    def GetAppears(him):
        return list(him.GetAppears)
    
    #destructive 
    
    @parameter('path', t_str)
    @parameter('value', t_str)
    @result(r_none)
    def SetValue(him, path, value):
        him.SetValue(path, value)
        IBase.adapter.plugin_change_domain_value(him, path)
    

