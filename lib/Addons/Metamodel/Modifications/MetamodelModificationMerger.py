from lib.Addons.Metamodel.Modifications.ElementModificationMerger import CElementModificationMerger
from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder


class CMetamodelModificationMerger(object):

    __elementModificationMerger = CElementModificationMerger()
    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()

    def MergeMetamodels(self, parentMetamodel, childMetamodel):
        mergedElementModifications = self.__MergeElementModifications(parentMetamodel, childMetamodel)
        mergedMetamodel = self.__modifiedMetamodelBuilder.BuildMetamodel(childMetamodel.GetRootNode(), mergedElementModifications)
        return mergedMetamodel

    def __MergeElementModifications(self, parentMetamodel, childMetamodel):
        parentElementModifications = parentMetamodel.GetElementFactory().GetModifications()
        childElementModifications = childMetamodel.GetElementFactory().GetModifications()
        return self.__elementModificationMerger.MergeModifications(parentElementModifications, childElementModifications)