from NodeEvalWrapper import CNodeEvalWrapper
from ConfigEvalWrapper import CConfigEvalWrapper
from grammar import parser as p
from lib.Base import CBaseObject

class CParamEval(CBaseObject):
    def __init__(self, str_, domain, type_ = None):
        try:
            self.__ast = p.parse(str_)
            vars_ = dict(
                self=None,
                cfg=CConfigEvalWrapper(),
                _line=None
            )
            evaltype = p.checktype2(self.__ast, vars_)
        except Exception as e:
            # TODO remove exception
            print "Error parsing:", str_
            print e
            print type_

        #if evaltype != type_:
        #    raise TypeError("Element attribute in metamodel have bad type: {0}, {1}".format(evaltype, type_))
        self.__type = type_

    def __call__(self, context):
        locals = dict(
            self = CNodeEvalWrapper(context.GetDomainObject(), context.GetProjectNode()),
            cfg = CConfigEvalWrapper(),
            _line = context.GetLine(),
        )
        locals.update(context.GetVariables())
        #value = eval(self.__code, locals, {'__builtins__': {}})
        #value = p.evalexp(self.__exp, locals)
        value = p.evalexp2(self.__ast, locals)

        if self.__type is not None:
            value = self.__type(value)
        return value

def BoolWrap(value):
    if isinstance(value, (str, unicode)):
        return value.lower() in ('true', 'yes', '1')
    return bool(value)

def FloatWrap(value):
    if isinstance(value, (str, unicode)):
        if ':' in value:
            value = value.split(':')
            if len(value) != 2:
                raise Exception("bad value")
            return float(int(value[0]))/int(value[1])
        elif value[-1] == '%':
            return float(value[:-1])/100
    return float(value)

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

def BuildParam(value, domain, type = None):
    if type is bool:
        type2 = BoolWrap
    elif type is float:
        type2 = FloatWrap
    elif isinstance(type, tuple):
        type2 = TupleWrap(type)
        type = tuple
    else:
        type2 = type
    if isinstance(value, (str, unicode)) and value.startswith('#'):
        if value.startswith('##'):
            if type2 is not None:
                return type2(value[1:])
            else:
                return value[1:]
        else:
            return CParamEval(value[1:], domain, type)
    elif type2 is not None:
        return type2(value)
    else:
        return value
