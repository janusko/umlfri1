import re

class Meta(type):
    
    interface = {}
    default_result = lambda self, x: x
    
    def __init__(self, name, bases, dictionary):
        type.__init__(self, name, bases, dictionary)
        if '__cls__' not in dictionary:
            return
        check = self.__checkclass(dictionary['__cls__'])
        self.interface[dictionary['__cls__']] = dict(
            (('__class__', self),) +
            tuple((fname, 
                {'params': self.__joindict(
                    {getattr(self, fname).func_code.co_varnames[0]: check}, 
                    dictionary[fname]._params if hasattr(dictionary[fname], '_params') else {}),
                 'result': dictionary[fname]._result if hasattr(dictionary[fname], '_result') else self.default_result})
            for fname in dictionary.iterkeys()
            if not fname.startswith('_') ))
        for fname, fun in dictionary.iteritems():
            if not fname.startswith('_'):
                setattr(self, fname, staticmethod(fun))
            
    @classmethod
    def GetMethod(self, cls, fname):
        cls = self.interface.get(cls)
        if cls and fname in cls:
            return (getattr(cls['__class__'], fname), cls[fname])
        else:
            return None
            
    
    @staticmethod
    def __checkclass(cls):
        def check(obj):
            if isinstance(obj, cls):
                return obj
            else:
                raise ValueError()
    
    @staticmethod
    def __joindict(d1, d2):
        d1.update(d2)
        return d2
