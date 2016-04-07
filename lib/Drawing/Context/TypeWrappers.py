from tree.evalvisitor import IObjectTypeWrapper, IOperationTypeWrapper, IAttributeTypeWrapper
import inspect

__author__ = 'Vincent Jurcisin-Kukla'


class ObjectTypeWrapper(IObjectTypeWrapper):
    def __init__(self, object__):
        super(ObjectTypeWrapper, self).__init__(object__)

    def __getattr__(self, item):
        obj = getattr(self.object, item)
        if inspect.ismethod(obj):   # method
            # TODO
            return OperationTypeWrapper()
        else:   # attribute
            # TODO
            return AttributeTypeWrapper()


class OperationTypeWrapper(IOperationTypeWrapper):
    def __init__(self, params, rtype):
        self.__rtype = rtype
        self.__params = params

    def rtype(self):
        return self.__rtype

    def args_generator(self):
        for i in self.__params:
            yield i


class AttributeTypeWrapper(IAttributeTypeWrapper):
    def attribute_type(self):
        pass