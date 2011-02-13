from .base import Base
from .primitiveType import primitiveTypes, PrimitiveType

class ExceptionProperty(Base):
    def __init__(self, name, exception, type, index, iterable = False, documentation = None):
        Base.__init__(self, name, exception)
        self.__documentation = documentation
        self.__iterable = iterable
        self.__index = index
        
        if type in primitiveTypes:
            self.__type = primitiveTypes[type]
        else:
            self.__type = type
    
    @property
    def exception(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def iterable(self):
        return self.__iterable
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def index(self):
        return self.__index
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if not isinstance(self.__type, PrimitiveType):
            self.__type = builder.getTypeByName(self.__type)
