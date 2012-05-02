from .baseContainer import BaseContainer
from .interfacePropertyThrows import InterfacePropertyThrows
from .interfaceMethod import InterfaceMethod
from .interfaceMethodParameter import InterfaceMethodParameter
from .interfaceMethodReturn import InterfaceMethodReturn
from .interfaceMethodThrows import InterfaceMethodThrows

from . import helper

class InterfacePropertyGetter(BaseContainer):
    def __init__(self, interfaceProperty, apiName = None):
        BaseContainer.__init__(self, None, interfaceProperty)
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computePropertyGetterApiName(self.singular, self.identifier)
    
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
    def throws(self):
        for child in self.children:
            if isinstance(child, InterfacePropertyThrows):
                yield child
    
    @property
    def index(self):
        return self.parent.index
    
    @property
    def identifier(self):
        return self.parent.identifier
    
    @property
    def fqn(self):
        return self.parent.fqn + '::' + '__get__'
    
    @property
    def apiName(self):
        return self.__apiName
    
    def createMethod(self, name = None):
        if name is None:
            name = self.name
        meth = InterfaceMethod(name, self.interfaceProperty.interface, apiName = self.apiName, documentation = self.interfaceProperty.documentation)
        
        if self.index is not None:
            InterfaceMethodParameter(self.index.name, meth, self.index.type, apiName = self.index.apiName, documentation = self.index.documentation)
        
        InterfaceMethodReturn(meth, self.type)
        
        for throw in self.throws:
            InterfaceMethodThrows(meth, throw.exception, throw.documentation)
        
        return meth
    
    def __repr__(self):
        return "<Getter of InterfaceProperty %s>"%(self.parent.fqn)
