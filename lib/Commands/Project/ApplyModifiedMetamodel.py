from ..Base.Command import CCommand, CommandNotDone
from lib.Addons.Metamodel.Modifications.MetamodelModificationMerger import CMetamodelModificationMerger
from lib.Elements.TypeSetter import CElementTypeSetter


class CApplyModifiedMetamodelCommand(CCommand):

    __elementTypeSetter = CElementTypeSetter()
    __metamodelModificationMerger = CMetamodelModificationMerger()

    def __init__(self, node, metamodel):
        CCommand.__init__(self)

        self.__node = node
        self.__metamodel = metamodel
        self.__newTypes = {}
        self.__oldTypes = {}

    def _Do(self):
        nodesToProcess = [(self.__node, self.__metamodel)]

        while len(nodesToProcess) > 0:
            node, metamodel = nodesToProcess.pop(0)
            if node.IsModifiedMetamodelRoot():
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
        return _('Apply modified metamodel on element') % (self.__node.GetName())