from lib.Addons.Metamodel.Modifications.ElementModificationBuilder import CElementModificationBuilder
from lib.Addons.Metamodel.Modifications.ModificationBundle import CMetamodelModificationBundle


class CMetamodelModificationBundleBuidler(object):

    def __init__(self):
        self.bundleBuilders = {}

    def CreateBundle(self, name):
        return self.bundleBuilders.setdefault(name, CElementModificationBuilder())

    def BuildBundles(self):
        return {name: CMetamodelModificationBundle(name, builder.GetElementTypeModifications()) for name, builder in self.bundleBuilders.iteritems()}