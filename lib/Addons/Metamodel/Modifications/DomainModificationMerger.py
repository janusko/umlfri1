class CDomainModificationBuilder(object):
    def MergeModifications(self, parentModifications, childModifications):
        return self.__MergeAttributeModifications(parentModifications, childModifications)
        # elementModificationsResolver = lambda parent, child: self.__MergeObjects(parent, child, self.__MergeAttributeModifications)
        # return self.__MergeObjects(parentModifications, childModifications, elementModificationsResolver)

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
    def __MergeAttributeModifications(parentModifications, childModifications):
        # TODO: optimize
        parentDict = {m.GetAttributeID(): m for m in parentModifications}
        childDict = {m.GetAttributeID(): m for m in childModifications}
        merged = CDomainModificationBuilder.__MergeObjects(parentDict, childDict, lambda parent, child: child)
        return merged.values()
