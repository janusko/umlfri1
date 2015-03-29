class CElementObjectTypeMapping(object):

    def __init__(self, object, type):
        self.object = object
        self.type = type

    def Apply(self):
        self.object.SetType(self.type)
        self.__ApplyDomainTypes(self.object.GetType().GetDomain(), self.object.GetDomainObject())

    def __ApplyDomainTypes(self, domainType, domainObject):
        factory = domainType.GetFactory()

        # change type, watchout of missing attributes?
        domainObject.SetType(domainType)

        for id in domainType.IterAttributeIDs():
            attrib = domainType.GetAttribute(id)

            if domainType.IsAtomic(id) and attrib['type'] != 'list':
                continue

            value = domainObject.GetValue(id)

            if attrib['type'] == 'list':
                itemType = factory.GetDomain(attrib['list']['type'])

                for obj in value:
                    self.__ApplyDomainTypes(itemType, obj)
            else:
                from lib.Domains import CDomainObject

                assert isinstance(value, CDomainObject)

                type = factory.GetDomain(domainType.GetName())

                self.__ApplyDomainTypes(type, value)
