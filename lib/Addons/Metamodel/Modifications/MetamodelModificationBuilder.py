from lib.Addons.Metamodel.Modifications.ElementModificationBuilder import CElementModificationBuilder
from lib.Addons.Metamodel.Modifications.ModificationBundle import CMetamodelModificationBundle
from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder


class CMetamodelModificationBuilder(object):

    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()

    def __init__(self, projectNode):
        self.projectNode = projectNode
        self.bundleBuilders = {}

    def CreateBundle(self, name):
        return self.bundleBuilders.setdefault(name, CElementModificationBuilder())

    def BuildMetamodel(self):
        bundles = self.__CreateModificationBundles()
        return self.__modifiedMetamodelBuilder.BuildMetamodel(self.projectNode, bundles)

    def __CreateModificationBundles(self):
        return {name: CMetamodelModificationBundle(name, builder.GetElementTypeModifications()) for name, builder in self.bundleBuilders.iteritems()}