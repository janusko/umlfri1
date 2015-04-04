class CElementModificationMerger(object):
    def MergeModifications(self, parentModifications, childModifications):
        mergedElementModifications = dict(parentModifications)
        for type, modifications in childModifications.iteritems():
            if type not in parentModifications:
                mergedElementModifications[type] = modifications
            else:
                parentDomainModifications = parentModifications[type]
                mergedElementModifications[type] = self.__MergeDomainModifications(parentDomainModifications, modifications)

        return mergedElementModifications

    def __MergeDomainModifications(self, parentModifications, childModifications):
        mergedDomainModifications = dict(parentModifications)

        for id, modification in childModifications:
            if id not in parentModifications:
                mergedDomainModifications[id] = modification
            else:
                parentAttributeModification = parentModifications[id]
                mergedDomainModifications[id] = self.__MergeAttributeModifications(parentAttributeModification, modification)

        return mergedDomainModifications

    def __MergeAttributeModifications(self, parentModification, childModification):
        return childModification