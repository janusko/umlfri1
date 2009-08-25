import re
from lib.Exceptions import *
from lib.Addons.Plugin.Client import classes
from lib.Addons.Plugin.Client.Proxy import CProxy

class Meta(type):
    
    interface = {}
    names = {}
    constructor = '__init__'
    implicit = lambda self, x: x
    
    def __init__(self, name, bases, dictionary):
        type.__init__(self, name, bases, dictionary)
        if not hasattr(self, '__cls__'):
            return
        if getattr(self, '__cls__') is not None:
            self.interface[dictionary['__cls__']] = dict(
                (('__class__', self),) +
                tuple((fname if not getattr(getattr(self, fname), '_constructor', False) else Meta.constructor, 
                    {'params': self.__joindict(
                        {getattr(self, fname).func_code.co_varnames[0]: self.implicit}, 
                        getattr(self, fname)._params if hasattr(getattr(self, fname), '_params') else {}),
                     'result': getattr(self, fname)._result,
                     'fname': fname,
                     'destructive': getattr(getattr(self, fname), '_destructive', False)
                    })
                for fname in dir(self)
                if (callable(getattr(self, fname)) 
                    and self.__valid_fname(fname) 
                    and not getattr(getattr(self, fname), '_not_iterface', False))))
            self.names[name] = dictionary['__cls__']
            classes[name] = type(name, (CProxy, ), {'Meta': Meta})
        for fname, fun in dictionary.iteritems():
            if callable(fun) and self.__valid_fname(fname):
                setattr(self, fname, staticmethod(fun))
            
    @classmethod
    def GetMethod(cls, hisclass, fname):
        if isinstance(hisclass, str):
            hisclass = cls.names.get(hisclass)
        desc = cls.interface.get(hisclass)
        if desc is not None and fname in desc:
            return getattr(desc['__class__'], desc[fname]['fname']), desc[fname]
        else:
            return None, None
    
    @classmethod
    def Execute(cls, obj, fname, params, isobject = True):
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
        params = dict((key, desc['params'][key](params[key])) for key in params)
        return desc['result'](fun(**params))
        
    @classmethod
    def Create(cls, hisclass, params):
        return cls.Execute(cls.names.get(hisclass), cls.constructor, params, False)
    
    @classmethod
    def GetMethodDescription(cls, classname, fname):
        dict = cls.interface.get(cls.names.get(classname))
        if dict is not None:
            return dict.get(fname)
    
    @classmethod
    def HasConstructor(cls, classname):
        return classname in cls.names and cls.constructor in cls.interface[cls.names[classname]]
        
    @classmethod
    def IsDestructive(cls, obj, fname):
        desc = cls.GetMethod(obj.__class__, fname)[1]
        if desc is None:
            raise UnknowMethodError()
        else:
            return desc['destructive']
            
    @classmethod
    def GetClassName(cls, object):
        desc = cls.interface.get(object.__class__)
        if desc:
            return desc['__class__'].__name__
        else:
            return None
    
    @classmethod
    def GetMethodList(cls, classname):
        desc = cls.interface.get(cls.names.get(classname))
        if desc is None:
            raise UnknownClassNameError(classname)
        return [name for name in desc if cls.__valid_fname(name)]
    
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
        return d1
    
    @staticmethod
    def __valid_fname(fname):
        return re.match(r'[a-zA-Z][a-zA-Z0-9_]+', fname) is not None
