from lib.Domains.TypeSetter import CDomainTypeSetter


class CElementTypeSetter(object):

    __domainTypeSetter = CDomainTypeSetter()

    def ApplyTypes(self, elementTypes):
        for element, type in elementTypes.iteritems():
            self.ApplyType(element, type)

    def ApplyType(self, element, type):
        element.SetType(type)
        self.__domainTypeSetter.ApplyType(element.GetDomainObject(), type.GetDomain())