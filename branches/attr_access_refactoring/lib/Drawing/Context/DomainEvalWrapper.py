from lib.Domains import CDomainObject

class CDomainEvalWrapper(object):
    def __init__(self, object):
        self.__object = object
    
    def __convert(self, val):
        if isinstance(val, CDomainObject):
            return CDomainEvalWrapper(val)
        elif isinstance(val, list):
            return CDomainEvalWrapper(val)
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
    
    def __len__(self):
        return len(self.__object)
