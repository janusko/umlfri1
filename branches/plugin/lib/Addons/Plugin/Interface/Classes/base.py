from lib.Addons.Plugin.Interface.meta import Meta
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import *

class IBase(object):
    __metaclass__ = Meta
    __cls__ = None
    adapter = None
    
    @classmethod
    @not_interface
    def SetAdapter(cls, adapter):
        cls.adapter = adapter
    
    @result(r_str)
    def GetClass(him):
        return Meta.GetClassName(him)
    
