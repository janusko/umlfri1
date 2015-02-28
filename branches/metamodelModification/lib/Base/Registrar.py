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
    
    def Clear(self):
        items = self.__dict.items()
        for key, value in items:
            if not getattr(value, '_persistent', False):
                value._ClearUID()
                del self.__dict[key]
        del items
    
    def _Register(self, uid, object):
        if uid in self.__dict:
            raise UIDException(("uidUsed", uid))
        self.__dict[uid] = object
        
    def __len__(self):
        return len(self.__dict)

registrar = CRegistrar()
