from ConfigEvalWrapper import CConfigEvalWrapper
from NodeEvalWrapper import CDrawingContextNodeEvalWrapper
from lib.ParameterEvaluation.ParamEval import CParamEval, CParamBuilder


class CDrawingContextParamEval(CParamEval):
    def _UpdateLocals(self, context, locals):
        node = context.GetProjectNode()

        locals['_line'] = context.GetLine()
        locals['cfg'] = CConfigEvalWrapper()
        locals['self'] = CDrawingContextNodeEvalWrapper(context.GetDomainObject(), node)
        if node is not None:
            locals['model'] = CDrawingContextNodeEvalWrapper(node.GetProject().GetDomainObject())

        locals.update(context.GetVariables())

class CDrawingContextParamBuilder(CParamBuilder):
    def _CreateParamEval(self, str, type):
        return CDrawingContextParamEval(str, type)

__paramBuilder = CDrawingContextParamBuilder()

def BuildParam(value, type = None):
    return __paramBuilder.BuildParam(value, type)