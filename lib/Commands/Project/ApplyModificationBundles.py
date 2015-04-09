import itertools
from ..Base.Command import CCommand, CommandNotDone
from lib.Addons.Metamodel.Modifications.MetamodelModificationMerger import CMetamodelModificationMerger
from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder
from lib.Elements.TypeSetter import CElementTypeSetter


class CApplyModificationBundlesCommand(CCommand):

    __elementTypeSetter = CElementTypeSetter()
    __metamodelModificationMerger = CMetamodelModificationMerger()
    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()

    def __init__(self, node, bundles):
        CCommand.__init__(self)

        self.__node = node
        self.__bundles = bundles
        self.__newTypes = {}
        self.__oldTypes = {}

    def _Do(self):
        parentMetamodel = None
        if self.__node.IsModifiedMetamodelRoot():
            parentMetamodel = self.__node.GetMetamodel().GetParentMetamodel()

            self.__bundles = list(itertools.chain(self.__node.GetMetamodel().GetModificationBundles(), self.__bundles))

        metamodel = self.__modifiedMetamodelBuilder.BuildMetamodel(self.__node, self.__bundles, parentMetamodel)
        nodesToProcess = [(self.__node, metamodel)]

        while len(nodesToProcess) > 0:
            node, metamodel = nodesToProcess.pop(0)
            if node.IsModifiedMetamodelRoot() and node != self.__node:
                # TODO: optimize - when both metamodels have same root, no need to merge
                metamodel = self.__metamodelModificationMerger.MergeMetamodels(metamodel, node.GetMetamodel())

            self.__newTypes[node] = metamodel.GetElementFactory().GetElement(node.GetType())
            self.__oldTypes[node] = node.GetObject().GetType()

            children = tuple((c, metamodel) for c in node.GetChilds())
            nodesToProcess.extend(children)

        self._Redo()

    def _Redo(self):
        self.__elementTypeSetter.ApplyTypes(self.__GetElementTypeDictionary(self.__newTypes))

    def _Undo(self):
        self.__elementTypeSetter.ApplyTypes(self.__GetElementTypeDictionary(self.__oldTypes))

    def __GetElementTypeDictionary(self, nodeTypes):
        return {node.GetObject(): type for node, type in nodeTypes.iteritems()}

    def GetGuiUpdates(self):
        return []

    def __str__(self):
        return _('Apply modification bundle on element "%s"') % (self.__node.GetName())