from ConfigEvalWrapper import CConfigEvalWrapper
from NodeEvalWrapper import CDrawingContextNodeEvalWrapper
from lib.ParameterEvaluation.ParamEval import CParamEval, CParamBuilder


class CDrawingContextParamEval(CParamEval):
    def _UpdateLocals(self, context, locals):
        locals['_line'] = context.GetLine()
        locals['cfg'] = CConfigEvalWrapper()

        locals.update(context.GetVariables())

    def _CreateNodeEvalWrapper(self, object, node):
        return CDrawingContextNodeEvalWrapper(object, node)

class CDrawingContextParamBuilder(CParamBuilder):
    def _CreateParamEval(self, str, type):
        return CDrawingContextParamEval(str, type)

__paramBuilder = CDrawingContextParamBuilder()

def BuildParam(value, type = None):
    return __paramBuilder.BuildParam(value, type)