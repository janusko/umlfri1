import weakref
from Type import CElementType


class CModifiedElementType(CElementType):

    def __init__(self, parentType, factory):
        self.parentType = parentType
        self.factory = lambda: factory

    def __getattribute__(self, item):
        if object.__getattribute__(self, '__dict__').has_key(item):
            return object.__getattribute__(self, item)

        if not hasattr(self.parentType, item):
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, item))

        obj = getattr(self.parentType, item)
        if hasattr(obj, '__call__'):
            def proxy_method(*args, **kwargs):
                return getattr(CElementType, item)(self, *args, **kwargs)

            return proxy_method
        else:
            return obj

