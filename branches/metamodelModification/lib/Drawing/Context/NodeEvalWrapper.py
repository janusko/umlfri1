from lib.ParameterEvaluation.NodeEvalWrapper import CNodeEvalWrapper

class CDrawingContextNodeEvalWrapper(CNodeEvalWrapper):

    _node = None

    def __init__(self, object, node = None):
        CNodeEvalWrapper.__init__(self, object)
        self._node = node

    def _CreateNodeEvalWrapper(self, object):
        return CDrawingContextNodeEvalWrapper(object)

    def _CreateCustomAttributes(self):
        yield '_Parent', self._Parent
        yield '_Icon', self._Icon
        yield '_Children', self._Children

    @property
    def _Parent(self):
        if not self._node:
            return None
        parent = self._node.GetParent()
        return CDrawingContextNodeEvalWrapper(parent.GetObject().GetDomainObject(), parent)

    @property
    def _Icon(self):
        if not self._node:
            return None
        return self._node.GetObject().GetType().GetIcon()

    @property
    def _Children(self):
        if self._node:
            for child in self._node.GetChilds():
                yield CDrawingContextNodeEvalWrapper(child.GetObject().GetDomainObject(), child)
