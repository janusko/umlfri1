from base import Base

import helper

class InterfacePropertyGetter(Base):
    def __init__(self, interfaceProperty, apiName = None):
        Base.__init__(self, None, interfaceProperty)
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
    def identifier(self):
        return self.parent.identifier
    
    @property
    def fqn(self):
        return self.parent.name + '::' + '__get__'
    
    @property
    def apiName(self):
        return self.__apiName
    
    def __repr__(self):
        return "<Getter of InterfaceProperty %s>"%(self.parent.fqn)
