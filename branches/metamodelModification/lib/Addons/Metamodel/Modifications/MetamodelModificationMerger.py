from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder


class CMetamodelModificationMerger(object):

    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()

    def MergeMetamodels(self, parentMetamodel, childMetamodel):
        modificationBundles = childMetamodel.GetModificationBundles()
        mergedMetamodel = self.__modifiedMetamodelBuilder.BuildMetamodel(childMetamodel.GetRootNode(), modificationBundles, parentMetamodel)
        return mergedMetamodel