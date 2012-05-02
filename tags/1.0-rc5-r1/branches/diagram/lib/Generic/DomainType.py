from GenericType import CGenericType

class CDomainType(CGenericType):
    
    def __init__(self, id, identity = None):
        
        CGenericType.__init__(self, id)
        self.identity = identity
        self.domain = None
        
    def GetDomain(self):
        '''
        @return: current domain type
        @rtype: L{CDomainType<lib.Domain.Type.CDomainType>}
        '''
        return self.domain
    
    def SetDomain(self, domain):
        '''
        Set current domain type
        
        @param domain: new domain type
        @type domain: L{CDomainType<lib.Domain.Type.CDomainType>}
        '''
        self.domain = domain
    
    def GetIdentity(self):
        
        return self.identity

