from base import Base

import helper

class InterfacePropertyIterator(Base):
    def __init__(self, interfaceProperty, apiName = None):
        Base.__init__(self, None, interfaceProperty)
        if apiName is not None:
            self.__apiName = apiName
        else:
            self.__apiName = helper.computePropertyIteratorApiName(self.singular, self.identifier)
    
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
        return self.parent.name + '::' + '__iter__'
    
    @property
    def apiName(self):
        return self.__apiName
    
    def __repr__(self):
        return "<Iterator of InterfaceProperty %s>"%(self.parent.fqn)
