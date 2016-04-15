from lib.Domains import CDomainObject
from lib.Base import CBaseObject


class CEvalWrapper(CBaseObject):
    def __init__(self, obj):
        self.__object = obj

    def __len__(self):
        return len(self.__object)

    def __convert(self, val):
        if isinstance(val, CDomainObject) or isinstance(val, list):
            return CEvalWrapper(val)
        else:
            return val
    
    def __getattr__(self, name):
        return self.__convert(self.__object.GetValue(name))
    
    def __getitem__(self, name):
        return self.__convert(self.__object[name])

    def __iter__(self):
        if isinstance(self.__object, CDomainObject):
            for name, val in self.__object:
                yield name, self.__convert(val)
        else:
            for val in self.__object:
                yield self.__convert(val)