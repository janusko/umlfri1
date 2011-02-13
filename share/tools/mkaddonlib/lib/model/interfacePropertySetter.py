from .base import Base

from . import helper

class InterfacePropertySetter(Base):
    def __init__(self, interfaceProperty, apiName = None, transactional = True):
        Base.__init__(self, None, interfaceProperty)
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computePropertySetterApiName(self.singular, self.identifier)
        self.__transactional = transactional
    
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
    def index(self):
        return self.parent.index
    
    @property
    def identifier(self):
        return self.parent.identifier
    
    @property
    def fqn(self):
        return self.parent.fqn + '::' + '__set__'
    
    @property
    def apiName(self):
        return self.__apiName
    
    @property
    def transactional(self):
        return self.__transactional
    
    def __repr__(self):
        return "<Setter of InterfaceProperty %s>"%(self.parent.fqn)
