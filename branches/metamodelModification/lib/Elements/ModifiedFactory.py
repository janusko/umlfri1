import weakref
from lib.Elements import CElementFactory


class CModifiedElementFactory(CElementFactory):
    def __init__(self, parentFactory, metamodel, modificatons):
        self.parentFactory = weakref.ref(parentFactory)
        self.metamodel = lambda: metamodel
        self.types = {}
        self.modifications = modificatons

    def GetModifications(self):
        return self.modifications

    def __getattribute__(self, item):
        if object.__getattribute__(self, '__dict__').has_key(item):
            return object.__getattribute__(self, item)

        if not hasattr(self.parentFactory(), item):
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, item))

        obj = getattr(self.parentFactory(), item)
        if hasattr(obj, '__call__'):
            def proxy_method(*args, **kwargs):
                return getattr(CModifiedElementFactory, item)(self, *args, **kwargs)

            return proxy_method
        else:
            return obj

