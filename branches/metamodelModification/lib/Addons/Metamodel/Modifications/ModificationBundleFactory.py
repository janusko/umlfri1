from distutils.command.build import build
from lib.Addons.Metamodel.Modifications.ModificationBundleBuilder import CMetamodelModificationBundleBuilder
from lib.Domains.AttributeConditions import BuildParam


class CModificationBundleFactory(object):

    defaultAttributeProperties = {
        'default': None,
        'hidden': False
    }

    @classmethod
    def CreateFromList(cls, list):
        builder = CMetamodelModificationBundleBuilder()
        for bundleName, bundleDict in list:
            bundleBuilder = builder.CreateBundle(bundleName)

            for domain, modifications in bundleDict.iteritems():
                for m in modifications:
                    attributeID =  m['attribute_id']
                    attributeProperties = m['attribute_properties']
                    if 'condition' in attributeProperties:
                        attributeProperties['condition'] = BuildParam(attributeProperties['condition'])

                    cls.__SetDefaultAttributeProperties(attributeProperties)
                    bundleBuilder.AddDomainAttribute(domain, attributeID, attributeProperties)

        return builder.BuildBundles()

    @classmethod
    def __SetDefaultAttributeProperties(cls, props):
        for name, value in cls.defaultAttributeProperties.iteritems():
            props.setdefault(name, value)