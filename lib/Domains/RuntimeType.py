import weakref
from lib.Domains import CDomainType
from lib.Domains.AttributeConditions import CAttributeEvaluationContext
from lib.Domains.AttributeConditions.ParamEval import CAttributeConditionParamEval


class CRuntimeDomainType(CDomainType):
    def __init__(self, parentType, object):
        self.parentType = lambda: parentType
        self.object = object

    def GetParentType(self):
        return self.parentType()

    def HasAttribute(self, id):
        return self.__GetAttributeInternal(id) is not None

    def GetAttribute(self, id):
        attribute = self.__GetAttributeInternal(id)
        if attribute is None:
            raise KeyError("Invalid attribute ID: {0}".format(id))

        return attribute

    def IterAttributeIDs(self):
        attributes = self.__GetParentProxyMethod(CDomainType.IterAttributeIDs)()
        for id in attributes:
            attribute = self.__GetParentProxyMethod(CDomainType.GetAttribute)(id)
            if self.__EvaluateAttributeCondition(attribute):
                yield id

    def __GetAttributeInternal(self, id):
        if self.__GetParentProxyMethod(CDomainType.HasAttribute)(id):
            attribute = self.__GetParentProxyMethod(CDomainType.GetAttribute)(id)
            if self.__EvaluateAttributeCondition(attribute):
                return attribute

        return None

    def __EvaluateAttributeCondition(self, attribute):
        if 'condition' in attribute:
            condition = attribute['condition']
            if isinstance(condition, CAttributeConditionParamEval):
                context = CAttributeEvaluationContext(self.object)
                return condition(context)
            else:
                return condition
        else:
            return True


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
            elif len(obj.__code__.co_varnames) > 0 and obj.__code__.co_varnames[0] == 'self':
                def proxy_method(*args, **kwargs):
                    return obj.im_func(self, *args, **kwargs)

                return proxy_method
            else:
                return obj
        else:
            # anything other than function from parent type is returned verbatim
            return obj

    def __GetParentProxyMethod(self, method):
        parentFunction = getattr(self.parentType(), method.__name__)

        def proxy_method(*args, **kwargs):
            return parentFunction.im_func(self, *args, **kwargs)

        return proxy_method