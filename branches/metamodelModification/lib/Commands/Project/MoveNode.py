from ..Base.Command import CCommand, CommandNotDone
from lib.Elements.TypeSetter import CElementTypeSetter


class CMoveNodeCommand(CCommand):

    __elementTypeSetter = CElementTypeSetter()

    def __init__(self, node, newParent, newPosition):
        CCommand.__init__(self)

        self.__node = node
        self.__newParent = newParent
        self.__newPosition = newPosition
        self.__newTypes = {}
        self.__oldParent = None
        self.__oldPosition = None
        self.__oldTypes = {node: node.GetObject().GetType()}

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

        if isNewParentModified or isOldParentModified:
            self.__CreateObjectTypeMappings()

        self._Redo()

    def __CreateObjectTypeMappings(self):
        nodesToProcess = [(self.__node, self.__newParent.GetMetamodel())]

        def HasParentModifiedMetamodel(node):
            parent = node.GetParent()
            if parent is self.__oldParent:
                # when we ask for parent of node being moved, check metamodel of new parent
                # since we're examining state _after_ the change is done
                return self.__newParent.HasModifiedMetamodel()
            else:
                return self.__newTypes[parent].HasModifiedMetamodel()

        while len(nodesToProcess) > 0:
            node, metamodel = nodesToProcess.pop(0)
            if HasParentModifiedMetamodel(node) and node.IsModifiedMetamodelRoot():
                # TODO: merge
                pass
            else:
                self.__newTypes[node] = metamodel.GetElementFactory().GetElement(node.GetType())
                self.__oldTypes[node] = node.GetObject().GetType()

            children = tuple((c, metamodel) for c in node.GetChilds())
            nodesToProcess.extend(children)

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
