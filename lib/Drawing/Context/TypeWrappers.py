from lib.datatypes import MethodAttrTypes
from tree.evalvisitor import IObjectTypeWrapper, IOperationTypeWrapper, IAttributeTypeWrapper
import inspect

__author__ = 'Vincent Jurcisin-Kukla'


class ObjectTypeWrapper(IObjectTypeWrapper):
    def __init__(self, object_):
        super(ObjectTypeWrapper, self).__init__(object_)

    def __getattr__(self, item):
        obj = getattr(self.object, item)
        if inspect.ismethod(obj):   # method
            methodwrap = MethodAttrTypes().GetMethod(self.object_type, item)
            if methodwrap is not None:
                return OperationTypeWrapper(methodwrap[0], methodwrap[1])
            else:
                raise Exception("Missing wrapper of method: {0}".format(item))
        else:   # attribute
            # object = cfg
            # cfg.Styles.Element.TextFont
            return AttributeTypeWrapper()


class OperationTypeWrapper(IOperationTypeWrapper):
    def __init__(self, args, rtype):
        self.__args = args
        self.__rtype = rtype

    def rtype(self):
        return self.__rtype

    def args_generator(self):
        for i in self.__args:
            yield i


class AttributeTypeWrapper(IAttributeTypeWrapper):
    def attribute_type(self):
        pass