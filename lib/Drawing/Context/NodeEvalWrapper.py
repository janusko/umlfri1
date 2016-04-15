from lib.Base import CBaseObject


class NodeEvalWrapper(CBaseObject):
    def __init__(self, object, node):
        self.__object = object
        self.__node = node

    @property
    def children(self):
        if self.__node:
            for child in self.__node.GetChilds():
                yield NodeEvalWrapper(child.GetObject().GetDomainObject(), child)

    @property
    def icon(self):
        if not self.__node:
            return None
        return self.__node.GetObject().GetType().GetIcon()

    @property
    def label(self):
        return self.__object.GetName()

    @property
    def parent(self):
        if not self.__node:
            return None
        parent = self.__node.GetParent()
        return NodeEvalWrapper(parent.GetObject().GetDomainObject(), parent)