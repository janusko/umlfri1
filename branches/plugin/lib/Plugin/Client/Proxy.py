import weakref
import thread
from Callable import CCallable


class CProxy(object):
    
    __objects = weakref.WeakValueDictionary()
    __lock = thread.allocate()
    
    def __init__(self, id, connection):
        self.id = id
        self.connection = connection
    
    def __getattr__(self, name):
        fun, desc = self.Meta.GetMethod(self.__class__.__name__, name)
        if fun is None:
            raise AttributeError()
        return CCallable(self.id, name, fun, desc, self.connection)
    
    def GetId(self):
        return self.id
