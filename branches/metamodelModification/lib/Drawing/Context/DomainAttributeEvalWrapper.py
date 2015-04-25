from lib.Domains import CDomainObject
from lib.Base import CBaseObject

class CDomainAttributeEvalWrapper(CBaseObject):

    __propertiesMap = {
        'Name': 'name',
        'Type': 'type',
        'IsHidden': 'hidden',
    }

    def __init__(self, attributeProperties):
        self.__attributeProperties = attributeProperties

    def __getattr__(self, name):
        if name not in self.__propertiesMap:
            raise TypeError("Attribute does not have property {0}".format(name))

        propName = self.__propertiesMap[name]
        return self.__attributeProperties[propName]