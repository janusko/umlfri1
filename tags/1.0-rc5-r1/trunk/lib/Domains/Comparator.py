from .Object import CDomainObject

class CDomainObjectPropertyChange(object):
    def __init__(self, path, oldValue, newValue):
        self.__path = path
        self.__oldValue = oldValue
        self.__newValue = newValue
    
    def GetCommand(self):
        return 'modify'
    
    def GetPath(self):
        return self.__path
    
    def GetOldValue(self):
        return self.__oldValue
    
    def GetNewValue(self):
        return self.__newValue

class CDomainObjectListAppend(object):
    def __init__(self, path, index, newValue):
        self.__path = path
        self.__index = index
        self.__newValue = newValue
    
    def GetCommand(self):
        return 'append'
    
    def GetPath(self):
        return self.__path
    
    def GetIndex(self):
        return self.__index
    
    def GetNewValue(self):
        return self.__newValue

class CDomainObjectListRemove(object):
    def __init__(self, path, index, oldValue):
        self.__path = path
        self.__index = index
        self.__oldValue = oldValue
    
    def GetCommand(self):
        return 'remove'
    
    def GetPath(self):
        return self.__path
    
    def GetIndex(self):
        return self.__index
    
    def GetOldValue(self):
        return self.__oldValue

class CDomainObjectComparator(object):
    def __init__(self, first, second):
        self.__first = first
        self.__second = second
        
        if first.GetType() is not second.GetType():
            raise Exception("Both domain objects has to be the same type")
    
    def __iter__(self):
        ret = []
        self.__compare(None, self.__first, self.__second, ret)
        
        return iter(ret)
    
    def __appendPath(self, path, attr = None, id = None):
        if attr is not None:
            if path is None:
                return attr
            else:
                return '%s.%s' % (path, attr)
        else:
            return '%s[%d]' % (path, id)
    
    def __compare(self, path, first, second, ret):
        if isinstance(first, CDomainObject):
            self.__compareStructs(path, first, second, ret)
        elif isinstance(first, list):
            self.__compareLists(path, first, second, ret)
        else:
            self.__compareAtomics(path, first, second, ret)
    
    def __compareStructs(self, path, first, second, ret):
        type = first.GetType()
        for attr in type.IterAttributeIDs():
            self.__compare(
                self.__appendPath(path, attr = attr),
                first.GetValue(attr),
                second.GetValue(attr),
                ret
            )
    
    def __compareLists(self, path, first, second, ret):
        for id, (valFirst, valSecond) in enumerate(zip(first, second)):
            self.__compare(
                self.__appendPath(path, id = id),
                valFirst,
                valSecond,
                ret
            )
        
        lenFirst = len(first)
        lenSecond = len(second)
        
        for id in xrange(lenFirst, lenSecond):
            ret.append(CDomainObjectListAppend(path, id, second[id]))
        
        for id in xrange(lenSecond, lenFirst):
            ret.append(CDomainObjectListRemove(path, id, first[id]))
    
    def __compareAtomics(self, path, first, second, ret):
        if first != second:
            ret.append(CDomainObjectPropertyChange(path, first, second))
