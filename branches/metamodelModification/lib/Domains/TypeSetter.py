class CDomainTypeSetter(object):
    def ApplyType(self, domainobject, domaintype):
        factory = domaintype.GetFactory()

        # change type, watch out of missing attributes?
        domainobject.SetType(domaintype)

        for id in domaintype.IterAttributeIDs():
            attrib = domaintype.GetAttribute(id)
            type = attrib['type']

            if domaintype.IsAtomic(id) and type != 'list':
                continue

            value = domainobject.GetValue(id)

            if type == 'list':
                itemType = factory.GetDomain(attrib['list']['type'])

                for obj in value:
                    self.ApplyType(obj, itemType)
            else:
                from lib.Domains import CDomainObject

                assert isinstance(value, CDomainObject)

                attributeDomainType = factory.GetDomain(type)

                self.ApplyType(value, attributeDomainType)