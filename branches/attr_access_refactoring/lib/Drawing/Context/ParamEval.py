from NodeEvalWrapper import CNodeEvalWrapper
from ConfigEvalWrapper import CConfigEvalWrapper

class CParamEval(object):
    def __init__(self, str, type = None):
        self.__code = compile(str, "<param>", 'eval')
        self.__type = type
    
    def __call__(self, context):
        locals = dict(
            self = CNodeEvalWrapper(context.GetDomainObject(), context.GetProjectNode()),
            cfg = CConfigEvalWrapper(),
            _line = context.GetLine(),
        )
        locals.update(context.GetVariables())
        
        value = eval(self.__code, locals, {'__builtins__': {}})
        if self.__type is not None:
            value = self.__type(value)
        return value

def BoolWrap(value):
    if isinstance(value, (str, unicode)):
        return value.lower() in ('true', 'yes', '1')
    return bool(value)

def TupleWrap(type):
    def tmp(value):
        out = []
        if isinstance(value, (str, unicode)):
            tmp = value.split()
        else:
            tmp = value
        for num, val in enumerate(tmp):
            out.append(type[num](val))
        return tuple(out)
    return tmp

def BuildParam(value, type = None):
    if type is bool:
        type = BoolWrap
    if isinstance(type, tuple):
        type = TupleWrap(type)
    if isinstance(value, (str, unicode)) and value.startswith('#'):
        if value.startswith('##'):
            if type is not None:
                return type(value[1:])
            else:
                return value[1:]
        else:
            return CParamEval(value[1:], type)
    elif type is not None:
        return type(value)
    else:
        return value
