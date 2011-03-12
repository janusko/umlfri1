from .base import Base
from .interfaceMethod import InterfaceMethod
from .interfaceMethodParameter import InterfaceMethodParameter
from .interfaceMethodReturn import InterfaceMethodReturn

from . import helper

class InterfacePropertyIterator(Base):
    def __init__(self, interfaceProperty, apiName = None):
        Base.__init__(self, None, interfaceProperty)
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computePropertyIteratorApiName(self.singular, self.identifier)
    
    @property
    def interfaceProperty(self):
        return self.parent
    
    @property
    def name(self):
        return self.parent.name
    
    @property
    def singular(self):
        return self.parent.singular
    
    @property
    def type(self):
        return self.parent.type
    
    @property
    def index(self):
        return self.parent.index
    
    @property
    def identifier(self):
        return self.parent.identifier
    
    @property
    def fqn(self):
        return self.parent.fqn + '::' + '__iter__'
    
    @property
    def apiName(self):
        return self.__apiName
    
    def createMethod(self, name = None):
        if name is None:
            name = self.name
        meth = InterfaceMethod(name, self.interfaceProperty.interface, apiName = self.apiName, documentation = self.interfaceProperty.documentation)
        
        InterfaceMethodReturn(meth, self.type, iterable = True)
        
        return meth
    
    def __repr__(self):
        return "<Iterator of InterfaceProperty %s>"%(self.parent.fqn)
