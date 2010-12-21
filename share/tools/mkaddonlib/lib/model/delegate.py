from baseContainer import BaseContainer
from delegateParameter import DelegateParameter
from delegateReturn import DelegateReturn

import helper

class Delegate(BaseContainer):
    def __init__(self, name, namespace, documentation = None):
        BaseContainer.__init__(self, name, namespace, sorted = False)
        self.__documentation = documentation
    
    @property
    def namespace(self):
        return self.parent
    
    @property
    def parameters(self):
        for child in self.children:
            if isinstance(child, DelegateParameter):
                yield child
    
    @property
    def returnType(self):
        for child in self.children:
            if isinstance(child, DelegateReturn):
                return child
    
    @property
    def documentation(self):
        return self.__documentation
