from .Decorators import params, mainthread, polymorphic

class IDomainType(object):
    def __init__(self, domainType):
        self.__domainType = domainType
    
    def GetName(self):
        return self.__domainType.GetName()
