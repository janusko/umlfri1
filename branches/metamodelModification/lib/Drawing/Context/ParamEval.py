from ConfigEvalWrapper import CConfigEvalWrapper
from NodeEvalWrapper import CDrawingContextNodeEvalWrapper
from lib.ParameterEvaluation.ParamEval import CParamEval, CParamBuilder


class CDrawingContextParamEval(CParamEval):
    def _UpdateLocals(self, context, locals):
        node = context.GetProjectNode()

        locals['_line'] = context.GetLine()
        locals['cfg'] = CConfigEvalWrapper()
        locals['self'] = CDrawingContextNodeEvalWrapper(context.GetDomainObject(), self._CreateCustomAttributes(), node)
        if node is not None:
            locals['model'] = CDrawingContextNodeEvalWrapper(node.GetProject().GetDomainObject(), self._CreateCustomAttributes())

        locals.update(context.GetVariables())

class CDrawingContextParamBuilder(CParamBuilder):
    def _CreateParamEval(self, str, type, createCustomAttributes=False):
        return CDrawingContextParamEval(str, type, createCustomAttributes)

__paramBuilder = CDrawingContextParamBuilder()

def BuildParam(value, type = None):
    return __paramBuilder.BuildParam(value, type)