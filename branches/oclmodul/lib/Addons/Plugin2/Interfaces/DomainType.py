from .Decorators import params, mainthread, polymorphic

class IDomainType(object):
    def __init__(self, domainType):
        self.__domainType = domainType
    
    @property
    def uid(self):
        return self.__domainType.GetUID()
    
    def GetName(self):
        return self.__domainType.GetName()
