from lib.Addons.Plugin.Interface.meta import Meta
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import r_str

class IBase(object):
    __metaclass__ = Meta
    __cls__ = None
    adapter = None
    
    @classmethod
    @not_interface
    def SetAdapter(cls, adapter):
        cls.adapter = adapter
        
    @classmethod
    @not_interface
    def GetAdapter(cls):
        return cls.adapter
    
    @result(r_str)
    def GetClass(him):
        return Meta.GetClassName(him)
    
