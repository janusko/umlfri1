from lib.Drawing.Context.DomainAttributesEvalWrapper import CDomainAttributesEvalWrapper
from lib.ParameterEvaluation.NodeEvalWrapper import CNodeEvalWrapper

class CDrawingContextNodeEvalWrapper(CNodeEvalWrapper):

    _node = None

    def __init__(self, object, createCustomAttributes, node = None):
        CNodeEvalWrapper.__init__(self, object, createCustomAttributes)
        self._node = node

    def _CreateNodeEvalWrapper(self, object, node=None):
        return CDrawingContextNodeEvalWrapper(object, self._createCustomAttributes, node or self._node)

    def _CreateCustomAttributes(self):
        yield '_Parent', self._Parent
        yield '_Icon', self._Icon
        yield '_Children', self._Children
        yield '_Attributes', self._Attributes

    @property
    def _Attributes(self):
        return CDomainAttributesEvalWrapper(self._object.GetType())

    @property
    def _Parent(self):
        if not self._node:
            return None
        parent = self._node.GetParent()
        return self._CreateNodeEvalWrapper(parent.GetObject().GetDomainObject(), parent)

    @property
    def _Icon(self):
        if not self._node:
            return None
        return self._node.GetObject().GetType().GetIcon()

    @property
    def _Children(self):
        if self._node:
            for child in self._node.GetChilds():
                yield self._CreateNodeEvalWrapper(child.GetObject().GetDomainObject(), child)
