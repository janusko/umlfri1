from ..Base.Command import CCommand, CommandNotDone
from lib.Addons.Metamodel.Modifications.MetamodelModificationMerger import CMetamodelModificationMerger
from lib.Addons.Metamodel.Modifications.ModificationTreeBuilder import CModificationTreeBuilder
from lib.Elements.TypeSetter import CElementTypeSetter


class CMoveNodeCommand(CCommand):

    __elementTypeSetter = CElementTypeSetter()
    __metamodelModificationMerger = CMetamodelModificationMerger()

    # root == root of subtree being moved (i.e. node being moved)
    # We need builder that DOES merge metamodel at root node, because new parent could have modified metamodel
    # and at the same time the node that is being moved is a root for new modified metamodel.
    # Then we need to perform metamodel merge at that node.
    __modificationTreeBuilder = CModificationTreeBuilder(True)

    def __init__(self, node, newParent, newPosition):
        CCommand.__init__(self)

        self.__node = node
        self.__newParent = newParent
        self.__newPosition = newPosition
        self.__newTypes = None
        self.__oldParent = None
        self.__oldPosition = None
        self.__oldTypes = None

    def _Do(self):
        if self.__newParent is None:
            raise CommandNotDone # TODO: more verbose error

        self.__oldParent = self.__node.GetParent()

        if self.__oldParent is None:
            raise CommandNotDone # TODO: more verbose error

        self.__oldPosition = self.__oldParent.GetChildIndex(self.__node)

        if self.__oldParent is self.__newParent and self.__oldPosition == self.__newPosition:
            raise CommandNotDone

        parent = self.__newParent
        while parent is not None:
            if parent is self.__node:
                raise CommandNotDone # TODO: more verbose error
            parent = parent.GetParent()

        isNewParentModified = self.__newParent.HasModifiedMetamodel()
        isOldParentModified = self.__oldParent.HasModifiedMetamodel()

        # when only node being moved has modified metamodel, there is no need to change element types
        if isNewParentModified or isOldParentModified:
            self.__newTypes, self.__oldTypes =\
                self.__modificationTreeBuilder.CreateObjectTypeMappings(self.__node,
                                                                        self.__newParent.GetMetamodel())
        self._Redo()

    def _Redo(self):
        self.__oldParent.RemoveChild(self.__node)
        self.__newParent.AddChild(self.__node, pos = self.__newPosition)
        if self.__newTypes:
            self.__elementTypeSetter.ApplyTypes(self.__GetElementTypeDictionary(self.__newTypes))

    def _Undo(self):
        self.__newParent.RemoveChild(self.__node)
        self.__oldParent.AddChild(self.__node, pos = self.__oldPosition)
        if self.__newTypes:
            self.__elementTypeSetter.ApplyTypes(self.__GetElementTypeDictionary(self.__oldTypes))

    def __GetElementTypeDictionary(self, nodeTypes):
        return {node.GetObject(): type for node, type in nodeTypes.iteritems()}

    def GetGuiUpdates(self):
        return [
            ('moveNodeInProject', (self.__node, self.__oldParent, self.__newParent))
        ]

    def __str__(self):
        return _("Element %s moved in project tree") % (self.__node.GetName())
