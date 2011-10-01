from .base import Base
from .primitiveType import primitiveTypes, PrimitiveType

from . import helper

class InterfaceMethodThrows(Base):
    def __init__(self, interfaceProperty, exception, documentation = None):
        Base.__init__(self, None, interfaceProperty)
        
        self.__exception = exception
        self.__documentation = documentation
    
    @property
    def interfaceProperty(self):
        return self.parent
    
    @property
    def exception(self):
        return self.__exception
    
    @property
    def fqn(self):
        return self.parent.fqn + "::__throws__(" + self.exception.fqn + ")"
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        yield self.__exception
    
    def __repr__(self):
        return "<Throws %s from InterfaceProperty %s>"%(self.exception.fqn, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        self.__exception = builder.getTypeByName(self.__exception)
