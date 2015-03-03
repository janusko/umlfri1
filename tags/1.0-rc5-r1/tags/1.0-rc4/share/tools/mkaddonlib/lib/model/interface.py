from .baseContainer import BaseContainer

class Interface(BaseContainer):
    def __init__(self, name, namespace, base = None, abstract = False, generate = True, documentation = None):
        BaseContainer.__init__(self, name, namespace)
        
        self.__base = base
        self.__abstract = abstract
        self.__generate = generate
        self.__documentation = documentation
    
    @property
    def namespace(self):
        return self.parent
    
    @property
    def base(self):
        return self.__base
    
    @property
    def isAbstract(self):
        return self.__abstract
    
    @property
    def generate(self):
        return self.__generate
    
    @property
    def documentation(self):
        return self.__documentation
    
    def _link(self, builder):
        BaseContainer._link(self, builder)
        
        if self.__base is not None:
            self.__base = builder.getTypeByName(self.__base)