from .base import Base
from .primitiveType import primitiveTypes, PrimitiveType

from . import helper

class InterfaceMethodReturn(Base):
    def __init__(self, interfaceMethod, type, iterable = False, documentation = None):
        Base.__init__(self, None, interfaceMethod)
        
        self.__iterable = iterable
        
        if type in primitiveTypes:
            self.__type = primitiveTypes[type]
        else:
            self.__type = type
        
        self.__documentation = documentation
    
    @property
    def interfaceMethod(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def fqn(self):
        return self.parent.fqn + "::__return__"
    
    @property
    def iterable(self):
        return self.__iterable
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        if not isinstance(self.__type, PrimitiveType):
            yield self.__type
    
    def __repr__(self):
        return "<ReturnType of InterfaceMethod %s>"%(self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if not isinstance(self.__type, PrimitiveType):
            self.__type = builder.getTypeByName(self.__type)
