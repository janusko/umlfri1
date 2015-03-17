from lib.Exceptions import DomainFactoryError

class CModifiedDomainFactory():
    def GetDomain(self, id):
        """
        @return: Domain type by name
        @rtype: L{CDomainType<Type.CDomainType>}

        @param id: Element type name
        @type  id: string
        """
        if id is None:
            return self.startPageDomain

        if not id in self.domains:
            raise DomainFactoryError('unrecognized domain name "%s"' % id)

        return self.domains[id]

    def IterTypes(self):
        '''
        iterator over domain types

        @rtype: L{CDomainType<CDomainType>}
        '''
        for type in self.domains.itervalues():
            yield type

    def HasDomain(self, id):
        '''
        @return: True if domain identifier is registered in current factory
        @rtype: bool

        @param id: Element type name
        @type  id: string
        '''
        return id in self.domains
