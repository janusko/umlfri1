from lib.Addons.Metamodel.Modifications.DomainModificationBuilder import CDomainModificationBuilder
from lib.Addons.Metamodel.Modifications.ModificationBundle import CMetamodelModificationBundle


class CMetamodelModificationBundleBuidler(object):

    def __init__(self):
        self.bundleBuilders = {}

    def CreateBundle(self, name):
        return self.bundleBuilders.setdefault(name, CDomainModificationBuilder())

    def BuildBundles(self):
        return [CMetamodelModificationBundle(name, None, builder.GetDomainModifications()) for name, builder in self.bundleBuilders.iteritems()]