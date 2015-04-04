import weakref
from lib.Addons.Metamodel.Metamodel import CMetamodel
from lib.Elements.ModifiedFactory import CModifiedElementFactory


class CModifiedMetamodel(CMetamodel):
    def __init__(self, parentMetamodel, rootNode, elementModifications, ownedElementModifications):
        self.parentMetamodel = weakref.ref(parentMetamodel)
        self.rootNode = rootNode
        self.elementFactory = CModifiedElementFactory(parentMetamodel.GetElementFactory(), self, elementModifications, ownedElementModifications)

    def GetRootNode(self):
        return self.rootNode

    def IsModified(self):
        return True

    def GetElementFactory(self):
        return self.elementFactory

    def __getattribute__(self, item):
        # special cases, don't know how to address these more properly
        if item == '__class__':
            return object.__getattribute__(self, item)

        # attribute saved in instance (e.g. self.factory)
        if object.__getattribute__(self, '__dict__').has_key(item):
            return object.__getattribute__(self, item)

        # attribute saved in class
        if self.__class__.__dict__.has_key(item):
            return object.__getattribute__(self, item)

        # by now we should now that the attribute is not in this class or this instance,\
        # so that remains only parent type
        if not hasattr(self.parentMetamodel(), item):
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, item))

        obj = getattr(self.parentMetamodel(), item)

        if hasattr(obj, '__call__'):
            # assume callable is bound method
            def proxy_method(*args, **kwargs):
                return getattr(CMetamodel, item)(self, *args, **kwargs)

            return proxy_method
        else:
            # anything other than function from parent type is returned verbatim
            return obj