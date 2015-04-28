from lib.Addons.Metamodel.Modifications.DomainModificationFactory import CDomainModificationFactory
from lib.Addons.Metamodel.Modifications.ModificationBundleBuilder import CMetamodelModificationBundleBuilder


class CModificationBundleFactory(object):

    @classmethod
    def CreateFromList(cls, list):
        builder = CMetamodelModificationBundleBuilder()
        for bundleDict in list:
            bundleName = bundleDict['name']
            bundleModificationsDict = bundleDict['modifications']
            bundleBuilder = builder.CreateBundle(bundleName)

            for domainModifications in bundleModificationsDict:
                domain = domainModifications['name']
                domainModifications = domainModifications['modifications']
                CDomainModificationFactory.CreateFromList(domain, domainModifications, bundleBuilder)

        return builder.BuildBundles()