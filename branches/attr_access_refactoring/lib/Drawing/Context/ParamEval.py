from DomainEvalWrapper import CDomainEvalWrapper 
from ConfigEvalWrapper import CConfigEvalWrapper 

class CParamEval(object):
    def __init__(self, str):
        self.__code = compile(str, "<param>", 'eval')
    
    def __call__(self, context):
        locals = dict(
            self = CDomainEvalWrapper(context.GetDomainObject()),
            cfg = CConfigEvalWrapper(),
            _line = context.GetLine(),
            _children = {},
        )
        locals.update(context.GetVariables())
        
        return eval(self.__code, locals, {'__builtins__': {}})
