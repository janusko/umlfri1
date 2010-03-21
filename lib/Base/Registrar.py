from weakref import WeakValueDictionary
from lib.Exceptions.DevException import UIDException

class CRegistrar(object):
    def __init__(self):
        self.__dict = WeakValueDictionary()
    
    def GetObject(self, uid):
        try:
            return self.__dict[uid]
        except KeyError:
            raise UIDException("objectNotFound")
    
    def _Register(self, uid, object):
        if uid in self.__dict:
            raise UIDException(("uidUsed", uid))
        self.__dict[uid] = object

registrar = CRegistrar()
