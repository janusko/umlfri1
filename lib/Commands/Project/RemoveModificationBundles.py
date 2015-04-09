import itertools
from ..Base.Command import CCommand, CommandNotDone
from lib.Addons.Metamodel.Modifications.ModificationTreeBuilder import CModificationTreeBuilder
from lib.Addons.Metamodel.Modifications.ModifiedMetamodelBuilder import CModifiedMetamodelBuilder
from lib.Elements.TypeSetter import CElementTypeSetter


class CRemoveModificationBundlesCommand(CCommand):

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
        if not self.__node.IsModifiedMetamodelRoot():
            raise CommandNotDone("Specified project node is not metamodel modification root, cannot remove modification bundles")

        metamodel = self.__node.GetMetamodel()
        bundles = metamodel.GetModificationBundles()
        newBundles = [bundle for bundle in bundles if bundle not in self.__bundles]

        parentMetamodel = metamodel.GetParentMetamodel()
        metamodel = self.__modifiedMetamodelBuilder.BuildMetamodel(self.__node, newBundles, parentMetamodel)

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