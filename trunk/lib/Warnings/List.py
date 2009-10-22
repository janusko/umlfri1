import warnings
import datetime
import linecache

class WarningList(object):
    __instance = None
    __old = None
    
    def __showwarning(self, message, category, filename, lineno, file = None, line = None):
        line = linecache.getline(filename, lineno) if line is None else line
        self.__list.append((datetime.datetime.now(), message, category, filename, lineno, line))
    
    def __getitem__(self, item):
        return self.__list[item]
    
    def __iter__(self):
        return self.__list.__iter__()
    
    def __str__(self):
        return self.__list.__str__()
    
    def __repr__(self):
        return self.__list.__repr__()
    
    @classmethod
    def register(cls):
        cls.__old = warnings.showwarning
        warnings.showwarning = cls().__showwarning
    
    @classmethod
    def unregister(cls):
        warnings.showwarning = cls.__old
        cls.__old = None
    
    def __new__(self):
        self2 = WarningList.__instance
        if self2 is None:
            self = WarningList.__instance = object.__new__(self)
            self.__list = []
        else:
            self = self2
        
        return self
