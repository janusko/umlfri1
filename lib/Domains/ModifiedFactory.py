from lib.Exceptions import DomainFactoryError

class CModifiedDomainFactory():

    def __init__(self, parentFactory, modifiedTypes):
        self.parentFactory = parentFactory
        self.modifiedTypes = modifiedTypes

    def GetDomain(self, id):
        """
        @return: Domain type by name
        @rtype: L{CDomainType<Type.CDomainType>}

        @param id: Element type name
        @type  id: string
        """
        if id is None:
            raise DomainFactoryError('domain name cannot be None')

        if id in self.modifiedTypes:
            return self.modifiedTypes[id]

        if id in self.parentFactory.HasDomain(id):
            return self.parentFactory.GetDomain(id)

        raise DomainFactoryError('unrecognized domain name "%s"' % id)

    def IterTypes(self):
        '''
        iterator over domain types

        @rtype: L{CDomainType<CDomainType>}
        '''
        for id, type in self.parentFactory.iteritems():
            if id in self.modifiedTypes:
                yield self.modifiedTypes[id]
            else:
                yield type

    def HasDomain(self, id):
        '''
        @return: True if domain identifier is registered in current factory
        @rtype: bool

        @param id: Element type name
        @type  id: string
        '''
        return id in self.modifiedTypes or self.parentFactory.HasDomain(id)
