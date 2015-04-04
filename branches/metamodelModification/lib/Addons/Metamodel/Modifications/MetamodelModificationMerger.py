from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder


class CMetamodelModificationMerger(object):

    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()

    def MergeMetamodels(self, parentMetamodel, childMetamodel):
        elementTypeModifications = childMetamodel.GetElementFactory().GetOwnedModifications()
        mergedMetamodel = self.__modifiedMetamodelBuilder.BuildMetamodel(childMetamodel.GetRootNode(), elementTypeModifications, parentMetamodel)
        return mergedMetamodel