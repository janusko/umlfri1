class CElementModificationMerger(object):
    def MergeModifications(self, parentModifications, childModifications):
        attributeModificationResolver = lambda parent, child: child
        elementModificationsResolver = lambda parent, child: self.__MergeObjects(parent, child, attributeModificationResolver)
        return self.__MergeObjects(parentModifications, childModifications, elementModificationsResolver)

    def __MergeObjects(self, parentObjects, childObjects, mergeResolver):
        mergedObjects = dict(parentObjects)

        for id, child in childObjects:
            if id not in parentObjects:
                mergedObjects[id] = child
            else:
                parent = parentObjects[id]
                mergedObjects[id] = mergeResolver(parent, child)

        return mergedObjects