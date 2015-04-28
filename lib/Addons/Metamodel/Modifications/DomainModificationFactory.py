from lib.Addons.Metamodel.Modifications.DomainModificationBuilder import CDomainModificationBuilder
from lib.Domains.AttributeConditions import BuildParam

class AttributeModificationType:
    Replace = 'replace'
    Delete = 'delete'


class CDomainModificationFactory(object):

    defaultAttributeProperties = {
        'default': None,
        'hidden': False
    }

    @classmethod
    def CreateFromList(cls, domain, modifications, builder=None):
        if builder is None:
            builder = CDomainModificationBuilder()

        for m in modifications:
            attributeID =  m['attribute_id']
            modificationType = m['modification_type']
            if modificationType == AttributeModificationType.Delete:
                builder.DeleteDomainAttribute(domain, attributeID)
            elif modificationType == AttributeModificationType.Replace:
                attributeProperties = m['attribute_properties']
                if 'condition' in attributeProperties:
                    attributeProperties['condition'] = BuildParam(attributeProperties['condition'])

                cls.__SetDefaultAttributeProperties(attributeProperties)
                builder.AddDomainAttribute(domain, attributeID, attributeProperties)

        if len(modifications) == 0:
            builder.CreateDomain(domain)

        return builder.GetDomainModifications()

    @classmethod
    def __SetDefaultAttributeProperties(cls, props):
        for name, value in cls.defaultAttributeProperties.iteritems():
            props.setdefault(name, value)