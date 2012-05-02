from .baseContainer import BaseContainer

class Exception(BaseContainer):
    def __init__(self, name, namespace, number, base = None, documentation = None):
        BaseContainer.__init__(self, name, namespace)
        
        self.__documentation = documentation
        self.__base = base
        self.__number = number
    
    @property
    def namespace(self):
        return self.parent
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def base(self):
        return self.__base
    
    @property
    def number(self):
        return self.__number
    
    def _link(self, builder):
        BaseContainer._link(self, builder)
        
        if self.__base is not None:
            self.__base = builder.getTypeByName(self.__base)
