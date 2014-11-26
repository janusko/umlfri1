from .baseContainer import BaseContainer
from . import helper

class Interface(BaseContainer):
    def __init__(self, name, namespace, apiName = None, base = None, abstract = False, generate = True, documentation = None):
        BaseContainer.__init__(self, name, namespace)
        
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computeInterfaceApiName(self.identifier)
        
        self.__base = base
        self.__abstract = abstract
        self.__generate = generate
        self.__documentation = documentation
        self.__descendants = []
    
    @property
    def namespace(self):
        return self.parent
    
    @property
    def apiName(self):
        return self.__apiName
    
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
    
    @property
    def descendants(self):
        return tuple(self.__descendants)
    
    @property
    def allBases(self):
        ret = []
        if self.__base is not None:
            base = self.base
            while base is not None:
                ret.insert(0, base)
                base = base.base
        return tuple(ret)
    
    @property
    def referenced(self):
        ret = set()
        if self.__base is not None:
            ret.add(self.__base)
        
        for child in self.children:
            for type in child.referenced:
                ret.add(type)
        
        for obj in ret:
            yield obj
    
    def validate(self):
        BaseContainer.validate(self)
        
        if self.__base is not None and not self.__base.isAbstract:
            raise Exception("Base interface of %s is not marked as abstract" % self.fqn)
    
    def _link(self, builder):
        BaseContainer._link(self, builder)
        
        if self.__base is not None:
            self.__base = builder.getTypeByName(self.__base)
            
            if not isinstance(self, Interface):
                raise Exception
            
            self.__base.__descendants.append(self)
