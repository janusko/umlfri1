import re
from lib.Exceptions import *
#from lib.Plugin.Communication.ComSpec import *

class Meta(type):
    
    interface = {}
    names = {}
    default_result = lambda self, x: x
    constructor = '__init__'
    
    def __init__(self, name, bases, dictionary):
        type.__init__(self, name, bases, dictionary)
        if not hasattr(self, '__cls__'):
            return
        check = self.__checkclass(dictionary['__cls__'])
        if getattr(self, '__cls__') is not None:
            self.interface[dictionary['__cls__']] = dict(
                (('__class__', self),) +
                tuple((fname if not getattr(getattr(self, fname), '_constructor', False) else Meta.constructor, 
                    {'params': self.__joindict(
                        {getattr(self, fname).func_code.co_varnames[0]: check}, 
                        getattr(self, fname)._params if hasattr(getattr(self, fname), '_params') else {}),
                     'result': getattr(self, fname)._result if hasattr(getattr(self, fname), '_result') else self.default_result,
                     'fname': fname})
                for fname in dir(self)
                if (callable(getattr(self, fname)) 
                    and self.__valid_fname(fname) 
                    and not getattr(getattr(self, fname), '_not_iterface', False)
                ))
            )
            self.names[name] = dictionary['__cls__']
        for fname, fun in dictionary.iteritems():
            if callable(fun) and self.__valid_fname(fname):
                setattr(self, fname, staticmethod(fun))
            
    @classmethod
    def GetMethod(cls, hisclass, fname):
        desc = cls.interface.get(hisclass)
        if desc is not None and fname in desc:
            return getattr(desc['__class__'], desc[fname]['fname']), desc[fname]
        else:
            return None, None
    
    @classmethod
    def Execute(cls, obj, fname, params, isobject = True):
        print obj, fname, params, isobject
        if isobject:
            fun, desc = cls.GetMethod(obj.__class__, fname)
            if getattr(fun, '_constructor', False):
                raise UnknowMethodError()
        else:
            fun, desc = cls.GetMethod(obj, fname)
            if not getattr(fun, '_constructor', False):
                raise UnknowMethodError()
        if desc is None:
            raise UnknowMethodError()
        elif isobject:
            params[fun.func_code.co_varnames[0]] = obj
        else:
            params = dict(zip(fun.func_code.co_varnames, params))
        params = dict((key, desc['params'].get(key, lambda x: x)(params[key])) for key in params)
        print obj, fname, params, isobject
        return desc['result'](fun(**params))
        
    @classmethod
    def Create(cls, hisclass, params):
        return cls.Execute(cls.names.get(hisclass), cls.constructor, params, False)
    
    @classmethod
    def HasConstructor(cls, classname):
        return classname in cls.names and cls.constructor in cls.interface[cls.names[classname]]
            
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
    
    @staticmethod
    def __valid_fname(fname):
        return re.match(r'[a-zA-Z][a-zA-Z0-9_]+', fname) is not None
