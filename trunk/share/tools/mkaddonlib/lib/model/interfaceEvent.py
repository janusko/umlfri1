from .base import Base
from .delegate import Delegate

from . import helper

class InterfaceEvent(Base):
    def __init__(self, name, interface, apiName, type, documentation = None):
        Base.__init__(self, name, interface)
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computeEventApiName(self.identifier)
        self.__type = type
        self.__documentation = documentation
    
    @property
    def apiName(self):
        return self.__apiName
    
    @property
    def type(self):
        return self.__type
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        yield self.__type
    
    def _link(self, builder):
        Base._link(self, builder)
        
        delegate = builder.getTypeByName(self.__type)
        if not isinstance(delegate, Delegate):
            raise Exception
        
        self.__type = delegate
