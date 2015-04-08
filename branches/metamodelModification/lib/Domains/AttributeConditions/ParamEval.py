from lib.Domains.AttributeConditions.NodeEvalWrapper import CAttributeConditionEvalWrapper
from lib.ParameterEvaluation.ParamEval import CParamEval, CParamBuilder


class CAttributeConditionParamEval(CParamEval):
    def _UpdateLocals(self, context, locals):
        locals['self'] = CAttributeConditionEvalWrapper(context.GetDomainObject())

class CAttributeConditionParamBuilder(CParamBuilder):
    def _CreateParamEval(self, str, type):
        return CAttributeConditionParamEval(str, type)

__paramBuilder = CAttributeConditionParamBuilder()

def BuildParam(value):
    return __paramBuilder.BuildParam(value, bool)