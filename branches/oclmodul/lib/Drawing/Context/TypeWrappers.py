import inspect
from types import NoneType

from lib.config import types
from lib.datatypes import MethodAttrTypes, CColor, CFont
from tree.typevisitor import OperationTypeWrapper
from tree.typewrappers import IObjectTypeWrapper, CollectionType

__author__ = 'Vincent Jurcisin-Kukla'


class ObjectTypeWrapper(IObjectTypeWrapper):

    def getOperationTypes(self, target, selector):
        operationList = []
        try:
            obj = getattr(target, selector)
            if inspect.ismethod(obj):
                methodWrapper = MethodAttrTypes().GetMethod(target, selector)
                operationList.append(OperationTypeWrapper(methodWrapper[0], methodWrapper[1]))
        except Exception:
            pass
        return operationList

    def getAttributeType(self, target, attr):
        try:
            return getattr(target, attr)
        except Exception:
            return None


class ConfigTypeWrapper(object):
    def __init__(self, path=[]):
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
        type_ = None
        try:
            type_ = eval(self.__domainObject.GetAttribute(name)['type'])
            if type_ is list:
                if name == 'operations':
                    return CollectionType(list, CollectionType(str))
                else:
                    return CollectionType(list, str)
            return type_
        except KeyError:
            pass
        except:
            if type_ == 'text':
                return unicode
            elif type_ == 'color':
                return CColor
            elif type_ == 'font':
                return CFont
            else:
                return str


class NodeTypeWrapper(object):
    @property
    def children(self):
        return list

    @property
    def icon(self):
        return str

    @property
    def label(self):
        return str

    @property
    def parent(self):
        return NoneType