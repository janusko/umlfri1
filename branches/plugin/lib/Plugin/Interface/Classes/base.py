from lib.Plugin.Interface.meta import Meta

class IBase(object):
    __metaclass__ = Meta
    adapter = None
    
    @classmethod
    def SetAdapter(cls, adapter):
        cls.adapter = adapter
    
