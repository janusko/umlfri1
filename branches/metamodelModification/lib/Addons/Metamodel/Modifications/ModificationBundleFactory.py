from lib.Addons.Metamodel.Modifications.DomainModificationFactory import CDomainModificationFactory
from lib.Addons.Metamodel.Modifications.ModificationBundleBuilder import CMetamodelModificationBundleBuilder


class CModificationBundleFactory(object):

    @classmethod
    def CreateFromList(cls, list):
        builder = CMetamodelModificationBundleBuilder()
        for bundleName, bundleDict in list:
            bundleBuilder = builder.CreateBundle(bundleName)

            for domain, modifications in bundleDict.iteritems():
                CDomainModificationFactory.CreateFromList(domain, modifications, bundleBuilder)

        return builder.BuildBundles()