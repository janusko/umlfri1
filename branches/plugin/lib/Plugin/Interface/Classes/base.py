from lib.Plugin.Interface.meta import Meta
from lib.Plugin.Interface.decorators import *
from lib.Plugin.Communication.ComSpec import *

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
    
