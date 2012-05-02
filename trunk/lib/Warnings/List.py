import warnings
import datetime
import linecache
from lib.Base import CBaseObject

class WarningList(CBaseObject):
    __instance = None
    __old = None
    
    def __showwarning(self, message, category, filename, lineno, file = None, line = None):
        line = linecache.getline(filename, lineno) if line is None else line
        
        item = (datetime.datetime.now(), message, category, filename, lineno, line)
        
        self.__list.append(item)
        
        for cb, args in self.__callbacks:
            cb(item, *args)
    
    def __getitem__(self, item):
        return self.__list[item]
    
    def __iter__(self):
        return self.__list.__iter__()
    
    def __str__(self):
        return self.__list.__str__()
    
    def __repr__(self):
        return self.__list.__repr__()
    
    @classmethod
    def handle(cls):
        cls.__old = warnings.showwarning
        warnings.showwarning = cls().__showwarning
    
    @classmethod
    def restore(cls):
        warnings.showwarning = cls.__old
        cls.__old = None
    
    def connect(self, callback, *args):
        self.__callbacks.append((callback, args))
    
    def disconnect(self, callback):
        for id, (cb, args) in enumerate(self.__callbacks):
            if cb is callback:
                del self.__callbacks[id]
                
                return True
        
        return False
    
    def __new__(self):
        self2 = WarningList.__instance
        if self2 is None:
            self = WarningList.__instance = object.__new__(self)
            self.__list = []
            self.__callbacks = []
        else:
            self = self2
        
        return self
