import weakref
import thread

class Reference(object):
    
    __pluginIdReferences = weakref.WeakValueDictionary()
    __lastPluginId = 0
    __pluginIdLock = thread.allocate()
    __adapter = staticmethod(lambda: None)
    
    def __init__(self):
        Reference.__pluginIdLock.acquire()
        Reference.__pluginIdReferences[Reference.__lastPluginId] = self
        self.__pluginID = Reference.__lastPluginId
        Reference.__lastPluginId += 1
        Reference.__pluginIdLock.release()
    
    def GetPluginId(self):
        return self.__pluginID
    
    @classmethod
    def GetObject(cls, id):
        return Reference.__pluginIdReferences[id] if id in Reference.__pluginIdReferences else None
    
    @classmethod
    def SetAdapter(cls, proj):
        Reference.__adapter = weakref.ref(proj) if proj else lambda: None
        
    @classmethod
    def GetAdapter(cls):
        return Reference.__adapter()
