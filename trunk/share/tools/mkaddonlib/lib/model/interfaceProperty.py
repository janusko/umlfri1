from .baseContainer import BaseContainer
from .identifier import Identifier
from .interfacePropertyGetter import InterfacePropertyGetter
from .interfacePropertySetter import InterfacePropertySetter
from .interfacePropertyIterator import InterfacePropertyIterator
from .interfacePropertyIndex import InterfacePropertyIndex
from .primitiveType import primitiveTypes, PrimitiveType

class InterfaceProperty(BaseContainer):
    def __init__(self, name, interface, type, singular = None, documentation = None):
        BaseContainer.__init__(self, name, interface)
        self.__singular = Identifier(singular or name)
        self.__documentation = documentation
        
        if type in primitiveTypes:
            self.__type = primitiveTypes[type]
        else:
            self.__type = type
    
    @property
    def interface(self):
        return self.parent
    
    @property
    def getter(self):
        for child in self.children:
            if isinstance(child, InterfacePropertyGetter):
                return child
    
    @property
    def setter(self):
        for child in self.children:
            if isinstance(child, InterfacePropertySetter):
                return child
    
    @property
    def iterator(self):
        for child in self.children:
            if isinstance(child, InterfacePropertyIterator):
                return child
    
    @property
    def index(self):
        for child in self.children:
            if isinstance(child, InterfacePropertyIndex):
                return child
    
    @property
    def type(self):
        return self.__type
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def singular(self):
        return self.__singular
    
    @property
    def referenced(self):
        if not isinstance(self.__type, PrimitiveType):
            yield self.__type
        if self.index is not None and not isinstance(self.index.type, PrimitiveType):
            yield self.index.type
    
    def _link(self, builder):
        BaseContainer._link(self, builder)
        
        if not isinstance(self.__type, PrimitiveType):
            self.__type = builder.getTypeByName(self.__type)
