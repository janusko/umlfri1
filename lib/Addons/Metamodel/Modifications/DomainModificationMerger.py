from lib.Domains.Modifications.DomainAttributeModification import DomainAttributeModificationType
from lib.Domains.Modifications.ReplaceAttributeModification import CReplaceAttributeModification


class CDomainModificationMerger(object):

    def __init__(self, mergeEnumValues=True):
        self.mergeEnumValues = mergeEnumValues

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

    def MergeAttributeModifications(self, parentModifications, childModifications):
        # TODO: optimize
        parentDict = {m.GetAttributeID(): m for m in parentModifications}
        childDict = {m.GetAttributeID(): m for m in childModifications}
        merged = self.__MergeObjects(parentDict, childDict,
                                     lambda parent, child: self.MergeAttributeModification(parent, child))
        return merged.values()

    def MergeAttributeModification(self, parentModification, childModification):
        # TODO: refactor, define merge rules, at least for replacements:
        # e.g. enum -> enum (merge values), int -> int or float -> float (merge constraints)
        # if needed, extend modification bundles (in API and builder too) with merge options

        # don't merge, if both modifications are not replacements
        if not (parentModification.GetType() == DomainAttributeModificationType.REPLACE) and (
                    childModification.GetType() == DomainAttributeModificationType.REPLACE):

            return childModification

        parentProperties = parentModification.GetAttributeProperties()
        childProperties = childModification.GetAttributeProperties()

        # don't merge if both attributes are not enums
        if parentProperties['type'] != 'enum' or childProperties['type'] != 'enum':
            return childModification

        # merge enum values
        enumValues = set(parentProperties['enum'])
        enumValues.update(childProperties['enum'])

        # merge rest of attribute properties and use merged enum values
        properties = dict(parentProperties)
        properties.update(childProperties)
        properties['enum'] = list(enumValues)
        modification = CReplaceAttributeModification(parentModification.GetAttributeID(), properties)
        return modification