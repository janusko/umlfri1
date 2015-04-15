from types import MethodType
import weakref
from Type import CDomainType
from lib.Domains.Modifications import CReplaceAttributeModification


class CModifiedDomainType(CDomainType):

    def __init__(self, parentType, factory, modifications):
        self.parentType = weakref.ref(parentType)
        self.factory = lambda: factory
        self.modifications = modifications

    def GetModifications(self):
        return self.modifications

    def GetParentType(self):
        return self.parentType()

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
        # special cases, don't know how to address these properly
        if item == '__class__':
            return object.__getattribute__(self, item)

        # attribute saved in instance (e.g. self.factory)
        if object.__getattribute__(self, '__dict__').has_key(item):
            return object.__getattribute__(self, item)

        # attribute saved in class
        if self.__class__.__dict__.has_key(item):
            return object.__getattribute__(self, item)

        parentType = self.parentType()

        # by now we should now that the attribute is not in this class or this instance,\
        # so that remains only parent type
        if not hasattr(parentType, item):
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, item))

        obj = getattr(parentType, item)

        if hasattr(obj, '__call__'):
            if isinstance(obj, weakref.ref):
                return obj
            elif isinstance(obj, MethodType):
                return MethodType(obj.im_func, self)
            else:
                return obj
        else:
            # anything other than function from parent type is returned verbatim
            return obj