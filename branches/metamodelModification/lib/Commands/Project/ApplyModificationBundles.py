import itertools
from ..Base.Command import CCommand, CommandNotDone
from lib.Addons.Metamodel.Modifications.ModificationTreeBuilder import CModificationTreeBuilder
from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder
from lib.Elements.TypeSetter import CElementTypeSetter


class CApplyModificationBundlesCommand(CCommand):

    __elementTypeSetter = CElementTypeSetter()
    __modifiedMetamodelBuilder = CModifiedMetamodelBuilder()
    __modificationTreeBuilder = CModificationTreeBuilder(False)    # builder that doesn't merge metamodel at root node

    def __init__(self, node, bundles):
        CCommand.__init__(self)

        self.__node = node
        self.__bundles = bundles
        self.__newTypes = None
        self.__oldTypes = None

    def _Do(self):
        parentMetamodel = None
        if self.__node.IsModifiedMetamodelRoot():
            parentMetamodel = self.__node.GetMetamodel().GetParentMetamodel()

            self.__bundles = list(itertools.chain(self.__node.GetMetamodel().GetModificationBundles(), self.__bundles))

        metamodel = self.__modifiedMetamodelBuilder.BuildMetamodel(self.__node, self.__bundles, parentMetamodel)

        self.__newTypes, self.__oldTypes = self.__modificationTreeBuilder.CreateObjectTypeMappings(self.__node, metamodel)

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