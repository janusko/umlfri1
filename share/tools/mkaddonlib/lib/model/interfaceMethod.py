from baseContainer import BaseContainer
from interfaceMethodParameter import InterfaceMethodParameter
from interfaceMethodReturn import InterfaceMethodReturn

import helper

class InterfaceMethod(BaseContainer):
    def __init__(self, name, interface, apiName = None, documentation = None):
        BaseContainer.__init__(self, name, interface, sorted = False)
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computeMethodApiName(self.identifier)
        self.__documentation = documentation
    
    @property
    def fqn(self):
        return self.parent.fqn + "." + self.name
    
    @property
    def interface(self):
        return self.parent
    
    @property
    def parameters(self):
        for child in self.children:
            if isinstance(child, InterfaceMethodParameter):
                yield child
    
    @property
    def returnType(self):
        for child in self.children:
            if isinstance(child, InterfaceMethodReturn):
                return child
    
    @property
    def apiName(self):
        return self.__apiName
    
    @property
    def documentation(self):
        return self.__documentation
