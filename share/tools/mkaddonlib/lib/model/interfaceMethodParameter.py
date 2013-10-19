from .base import Base
from .primitiveType import primitiveTypes, PrimitiveType

from . import helper

class InterfaceMethodParameter(Base):
    def __init__(self, name, interfaceMethod, type, apiName = None, required = True, nullable = False, default = None, documentation = None):
        Base.__init__(self, name, interfaceMethod)
        
        self.__required = required
        self.__nullable = nullable
        
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computeMethodParameterApiName(self.identifier)
        
        if type in primitiveTypes:
            self.__type = primitiveTypes[type]
            
            if not self.__required:
                if default is None:
                    self.__default = None
                else:
                    self.__default = self.__type.convert(default)
            else:
                self.__default = None
        else:
            self.__type = type
            self.__default = None
        
        self.__documentation = documentation
    
    @property
    def interfaceMethod(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def apiName(self):
        return self.__apiName
    
    @property
    def fqn(self):
        return self.parent.fqn + "(" + self.name + ")"
    
    @property
    def required(self):
        return self.__required
    
    @property
    def nullable(self):
        return self.__nullable
    
    @property
    def default(self):
        return self.__default
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        if self.__type != '*' and not isinstance(self.__type, PrimitiveType):
            yield self.__type
    
    def __repr__(self):
        return "<Parameter %s of InterfaceMethod %s>"%(self.name, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if self.__type != '*' and not isinstance(self.__type, PrimitiveType):
            self.__type = builder.getTypeByName(self.__type)
