from lib.Addons.Metamodel.Modifications.ModificationBundleBuilder import CMetamodelModificationBundleBuilder
from lib.Exceptions import MetamodelModificationError


class CProjectNodeModificationBundleBuilder(object):

    def __init__(self, projectNode, bundleName):
        self.__projectNode = projectNode
        self.__modificationBundleBuilder = CMetamodelModificationBundleBuilder()
        self.__bundleBuilder = self.__modificationBundleBuilder.CreateBundle(bundleName)
        self.__bundle = None

    def GetNode(self):
        return self.__projectNode

    def ReplaceDomainAttribute(self, domain, attributeID, attributeProperties):
        self.__CheckBundle()

        self.__bundleBuilder.ReplaceDomainAttribute(domain, attributeID, attributeProperties)

    def RemoveDomainAttribute(self, domain, attributeID):
        self.__CheckBundle()

        self.__bundleBuilder.DeleteDomainAttribute(domain, attributeID)

    def Build(self):
        self.__CheckBundle()

        self.__bundle = self.__modificationBundleBuilder.BuildBundles()[0]
        return self.__bundle

    def __CheckBundle(self):
        if self.__bundle:
            raise MetamodelModificationError("Modification bundle {0} was already built, it cannot be modified".format(
                self.__bundle.GetName()))