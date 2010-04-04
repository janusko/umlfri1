import weakref
import thread
from Callable import CCallable


class CProxy(object):
    
    __objects = weakref.WeakValueDictionary()
    __lock = thread.allocate()
    
    def __new__(cls, id, connection):
        try:
            CProxy.__lock.acquire()
            if id in CProxy.__objects:
                return CProxy.__objects[id]
            else:
                obj = object.__new__(cls)
                CProxy.__objects[id] = obj
                return obj
        finally:
            CProxy.__lock.release()
    
    def __init__(self, id, connection):
        self.id = id
        self.connection = connection
    
    def __getattr__(self, name):
        fun, desc = self.Meta.GetMethod(self.__class__.__name__, name)
        if fun is None:
            raise AttributeError()
        return CCallable(self.id, name, self.connection)
    
    def __getattribute__(self, name):
        res = object.__getattribute__(self, name)
        if name == '__dict__':
            lst = self.Meta.GetMethodList(self.__class__.__name__)
            res.update(dict((item, self.__getattr__(item)) for item in lst))
        return res
    
    def GetId(self):
        return self.id
