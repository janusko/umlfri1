from base import Base
from primitiveType import primitiveTypes, PrimitiveType

import helper

class InterfaceMethodThrows(Base):
    def __init__(self, interfaceMethod, exception, documentation = None):
        Base.__init__(self, None, interfaceMethod)
        
        self.__exception = exception
        self.__documentation = documentation
    
    @property
    def interfaceMethod(self):
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
    
    def __repr__(self):
        return "<Throws %s from InterfaceMethod %s>"%(self.exception.fqn, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if not isinstance(self.__exception, PrimitiveType):
            self.__exception = builder.getTypeByName(self.__exception)
