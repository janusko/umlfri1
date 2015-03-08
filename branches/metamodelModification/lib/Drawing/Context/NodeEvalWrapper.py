from lib.ParameterEvaluation.NodeEvalWrapper import CNodeEvalWrapper

class CDrawingContextNodeEvalWrapper(CNodeEvalWrapper):

    def _CreateNodeEvalWrapper(self, object, node):
        return CDrawingContextNodeEvalWrapper(object, node)

    def _CreateCustomAttributes(self):
        yield '_Parent', self._Parent
        yield '_Icon', self._Icon

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
