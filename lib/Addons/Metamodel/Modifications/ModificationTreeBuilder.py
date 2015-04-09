from lib.Addons.Metamodel.Modifications.MetamodelModificationMerger import CMetamodelModificationMerger


class CModificationTreeBuilder(object):

    __metamodelModificationMerger = CMetamodelModificationMerger()

    def __init__(self, mergeMetamodelAtRoot):
        self.mergeMetamodelAtRoot = mergeMetamodelAtRoot

    def CreateObjectTypeMappings(self, rootNode, initialMetamodel):
        nodesToProcess = [(rootNode, initialMetamodel)]

        newTypes = {}
        oldTypes = {}

        while len(nodesToProcess) > 0:
            node, metamodel = nodesToProcess.pop(0)
            if node.IsModifiedMetamodelRoot() and (self.mergeMetamodelAtRoot or node != rootNode):
                # TODO: optimize - when both metamodels have same root, no need to merge
                metamodel = self.__metamodelModificationMerger.MergeMetamodels(metamodel, node.GetMetamodel())

            newTypes[node] = metamodel.GetElementFactory().GetElement(node.GetType())
            oldTypes[node] = node.GetObject().GetType()

            children = tuple((c, metamodel) for c in node.GetChilds())
            nodesToProcess.extend(children)

        return newTypes, oldTypes