from lib.Plugin.Interface.meta import Meta
from lib.Plugin.Interface.decorators import *

class IBase(object):
    __metaclass__ = Meta
    adapter = None
    
    @classmethod
    @not_interface
    def SetAdapter(cls, adapter):
        cls.adapter = adapter
    
