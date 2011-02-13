from .baseContainer import BaseContainer
from .interfaceMethodParameter import InterfaceMethodParameter
from .interfaceMethodReturn import InterfaceMethodReturn

from . import helper

class InterfaceMethod(BaseContainer):
    def __init__(self, name, interface, apiName = None, mutator = False, transactional = True, documentation = None):
        BaseContainer.__init__(self, name, interface, sorted = False)
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computeMethodApiName(self.identifier)
        self.__documentation = documentation
        self.__mutator = mutator
        self.__transactional = mutator and transactional
    
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
    def mutator(self):
        return self.__mutator
    
    @property
    def transactional(self):
        return self.__transactional
    
    @property
    def documentation(self):
        return self.__documentation
