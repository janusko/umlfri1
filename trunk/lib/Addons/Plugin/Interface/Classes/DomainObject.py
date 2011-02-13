from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Domains.Object import CDomainObject

class IDomainObject(IBase):
    __cls__ = None
    
    def GetName(him):
        return him.GetName()
    
    def GetValue(him, path):
            res = him.GetValue(path)
            if isinstance(res, CDomainObject):
                return str(res.GetSaveInfo())
            elif isinstance(res, list):
                return '[' + ','.join(str(i.GetSaveInfo()) for i in res) + ']'
            else:
                return str(res)
    
    def GetSaveInfo(him):
        return him.GetSaveInfo()
    
    def GetType(him):
        return him.GetType().GetId()
    
    def GetAppears(him):
        return list(him.GetAppears())
    
    #destructive 
    
    @destructive
    def SetValue(him, path, value):
        him.SetValue(path, value)
        IBase.adapter.plugin_change_domain_value(him, path)
        
    def GetDomainType(him):
        return him.GetDomainType()
    

