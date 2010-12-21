from base import Base
from primitiveType import primitiveTypes, PrimitiveType

import helper

class InterfacePropertyIndex(Base):
    def __init__(self, name, interfaceProperty, type, apiName = None, documentation = None):
        Base.__init__(self, name, interfaceProperty)
        
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computePropertyIndexApiName(self.identifier)
        
        if type in primitiveTypes:
            self.__type = primitiveTypes[type]
        else:
            self.__type = type
        
        self.__documentation = documentation
    
    @property
    def interfaceProperty(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def apiName(self):
        return self.__apiName
    
    @property
    def fqn(self):
        return self.parent.fqn + "[" + self.name + "]"
    
    @property
    def documentation(self):
        return self.__documentation
    
    def __repr__(self):
        return "<Index %s of InterfaceProperty %s>"%(self.name, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if not isinstance(self.__type, PrimitiveType):
            self.__type = builder.getTypeByName(self.__type)
