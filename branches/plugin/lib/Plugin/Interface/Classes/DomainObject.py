from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Domains.Object import CDomainObject

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
                return str(res.GetSaveInfo())
            elif isinstance(res, list):
                return '[' + ','.join(str(i.GetSaveInfo()) for i in res) + ']'
            else:
                return str(res)
    
    @result(r_str)
    def GetSaveInfo(him):
        return str(him.GetSaveInfo())
    
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
    

