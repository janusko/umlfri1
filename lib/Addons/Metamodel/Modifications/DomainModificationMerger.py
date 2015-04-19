class CDomainModificationMerger(object):
    def MergeModifications(self, parentModifications, childModifications):
        attributeModificationsResolver = lambda parent, child:  self.MergeAttributeModifications(parent, child)
        return self.__MergeObjects(parentModifications, childModifications, attributeModificationsResolver)

    @staticmethod
    def __MergeObjects(parentObjects, childObjects, mergeResolver):
        mergedObjects = dict(parentObjects)

        for id, child in childObjects.iteritems():
            if id not in parentObjects:
                mergedObjects[id] = child
            else:
                parent = parentObjects[id]
                mergedObjects[id] = mergeResolver(parent, child)

        return mergedObjects

    @staticmethod
    def MergeAttributeModifications(parentModifications, childModifications):
        # TODO: optimize
        parentDict = {m.GetAttributeID(): m for m in parentModifications}
        childDict = {m.GetAttributeID(): m for m in childModifications}
        merged = CDomainModificationMerger.__MergeObjects(parentDict, childDict, lambda parent, child: child)
        return merged.values()
