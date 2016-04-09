import inspect

from lib.config import types
from lib.Base import CBaseObject
from lib.datatypes import MethodAttrTypes
from tree.typevisitor import IObjectTypeWrapper, OperationTypeWrapper

__author__ = 'Vincent Jurcisin-Kukla'


class ObjectTypeWrapper(IObjectTypeWrapper):

    def getOperationType(self, target, selector):
        obj = getattr(target, selector)
        if inspect.ismethod(obj):
            methodWrapper = MethodAttrTypes().GetMethod(target, selector)
            if methodWrapper is not None:
                return OperationTypeWrapper(methodWrapper[0], methodWrapper[1])
            else:
                raise Exception("Doesn't exist operation wrapper for operation: {0}".format(selector))
        else:
            TypeError("Method: {0} doesn't exist on {1}".format(selector, target))

    def getAttributeType(self, target, attr):
        pass


class ConfigTypeWrapper(object):
    def __init__(self, path = []):
        self.__path = path

    def __getattr__(self, attr):
        path = self.__path + [attr]
        pathStr = '/' + '/'.join(path)
        if pathStr in types:
            return types[pathStr]
        else:
            return ConfigTypeWrapper(path)


class DomainTypeWrapper(object):
    def __init__(self, domainType):
        self.__domainObject = domainType

    def __getattr__(self, name):
        return eval(self.__domainObject.GetAttribute(name)['type'])
