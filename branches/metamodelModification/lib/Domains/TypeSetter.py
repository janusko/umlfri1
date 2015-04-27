from lib.Exceptions import DomainTypeError


class CDomainTypeSetter(object):
    def ApplyType(self, domainobject, domaintype):
        factory = domaintype.GetFactory()

        # change type, watch out of missing attributes?
        domainobject.SetType(domaintype)

        for id in domaintype.IterAttributeIDs():
            attrib = domaintype.GetAttribute(id)
            type = attrib['type']

            value = domainobject.GetValue(id, False)

            if domaintype.IsAtomic(id) and type != 'list':
                # hack to allow changing possible enum values for given enum attribute
                # when multiple values with different types for same attribute is implemented in
                # CDomainObject, this should be refactored (take into account that two enums can be different
                # and thus should be considered as value of different type)
                try:
                    domaintype.CheckValue(value, id)
                except DomainTypeError:
                    domainobject.SetValue(id, domaintype.GetDefaultValue(id), False)
                continue

            if type == 'list':
                itemTypeStr = attrib['list']['type']
                if domaintype.IsDomainAtomic(itemTypeStr):
                    continue

                itemType = factory.GetDomain(itemTypeStr)

                for obj in value:
                    self.ApplyType(obj, itemType)
            else:
                from lib.Domains import CDomainObject

                assert isinstance(value, CDomainObject)

                attributeDomainType = factory.GetDomain(type)

                self.ApplyType(value, attributeDomainType)