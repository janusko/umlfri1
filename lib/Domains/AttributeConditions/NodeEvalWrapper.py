from lib.ParameterEvaluation.NodeEvalWrapper import CNodeEvalWrapper

class CAttributeConditionEvalWrapper(CNodeEvalWrapper):

    def _CreateNodeEvalWrapper(self, object):
        return CAttributeConditionEvalWrapper(object)

    def _CreateCustomAttributes(self):
        yield '_Parent', self._Parent

    @property
    def _Parent(self):
        parent = self._object.GetParent()
        if parent is None:
            return None

        return self._CreateNodeEvalWrapper(parent)
