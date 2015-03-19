from lib.Exceptions import FactoryError


class CModifiedElementFactory:

    def __init__(self, parentFactory, types = None):
        self.parentFactory = parentFactory
        self.types = types or {}

    def GetElement(self, type):
        """
        Get element type by name

        @param type: Element type name
        @type  type: string
        """
        if id is None:
            raise FactoryError('element type name cannot be None')

        if id in self.types:
            return self.types[id]

        if id in self.parentFactory.HasType(id):
            return self.parentFactory.GetElement(id)

        raise FactoryError('unrecognized elementType name "%s"' % type)

    def IterTypes(self):
        '''
        iterator over element types

        @rtype: L{CElementType<CElementType>}
        '''
        for id in self.parentFactory.IterTypes():
            if id in self.types:
                yield self.types[id]
            else:
                yield type

        for id in self.types.iterkeys():
            if not self.parentFactory.HasType(id):
                yield self.types[id]

    def HasType(self, id):
        return id in self.types or self.parentFactory.HasType(id)
