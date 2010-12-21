from baseContainer import BaseContainer

class Exception(BaseContainer):
    def __init__(self, name, namespace, documentation = None):
        BaseContainer.__init__(self, name, namespace)
        
        self.__documentation = documentation
    
    @property
    def documentation(self):
        return self.__documentation
