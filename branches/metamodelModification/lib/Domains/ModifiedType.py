import weakref
from Type import CDomainType
from lib.Domains.Modifications import CReplaceAttributeModification


class CModifiedDomainType(CDomainType):

    def __init__(self, parentType, factory, modifications):
        self.parentType = weakref.ref(parentType)
        self.factory = lambda: factory
        self.modifications = modifications

    def AppendAttribute(self, id, name, type = None, default = None, hidden=False):
        properties = {'name': name, 'type': type, 'default': default, 'hidden': (hidden in ('true', '1'))}
        modification = CReplaceAttributeModification(id, properties)
        self.modifications.append(modification)

    def HasAttribute(self, id):
        return id in self._GetAttributes()

    def GetAttribute(self, id):
        return self._GetAttributes()[id]

    def IterAttributeIDs(self):
        for id in self._GetAttributes().iterkeys():
            yield id

    def _GetAttributes(self):
        attributes = dict(self.parentType()._GetAttributes())
        for m in self.modifications:
            m.ApplyToAttributes(attributes)

        return attributes

    def __getattribute__(self, item):
        if item == '__class__':
            return object.__getattribute__(self, item)

        if object.__getattribute__(self, '__dict__').has_key(item):
            return object.__getattribute__(self, item)

        if self.__class__.__dict__.has_key(item):
            return object.__getattribute__(self, item)

        if not hasattr(self.parentType(), item):
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, item))

        obj = getattr(self.parentType(), item)
        if hasattr(obj, '__call__'):
            def proxy_method(*args, **kwargs):
                return getattr(CDomainType, item)(self, *args, **kwargs)

            return proxy_method
        else:
            return obj