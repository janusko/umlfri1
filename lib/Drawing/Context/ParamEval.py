from ConfigEvalWrapper import CConfigEvalWrapper
from EvalWrapper import CEvalWrapper
from grammar import parser as p
from lib.Base import CBaseObject
from lib.Drawing.Context.NodeEvalWrapper import NodeEvalWrapper
from lib.Drawing.Context.TypeWrappers import ObjectTypeWrapper, ConfigTypeWrapper, DomainTypeWrapper, NodeTypeWrapper
from lib.Exceptions.UserException import MetamodelError


class CParamEval(CBaseObject):
    def __init__(self, str_, domainType, localvars, type_=None):
        self.__str = str_
        self.__type = type_
        try:
            self.__ast = p.parse(str_)
            vars_ = dict(
                self=DomainTypeWrapper(domainType),
                node=NodeTypeWrapper(),
                cfg=ConfigTypeWrapper(),
                _line=int
            )
            vars_.update(localvars)
            evaltype = p.checktype2(self.__ast, ObjectTypeWrapper(), vars_)
        except Exception as e:
            if type_ is not None:
                type_ = type_.__name__
            raise MetamodelError("Error during type checking: {0}. Checked string: '{1}', expected type: '{2}'."
                                 .format(e, str_, type_))

        if evaltype in (list, str) and type_ == bool:
            pass
        elif evaltype in (str, unicode) and type_ in (str, unicode):
            pass
        elif type_ is None:
            pass
        elif evaltype != type_:
            if evaltype is not None:
                evaltype = evaltype.__name__
            if type_ is not None:
                type_ = type_.__name__
            #print "Error: {0} != {1}    ON: {2}".format(evaltype, type_, str_)
            raise MetamodelError("Different types (domain type) {0} != {1} (expected type), checked string: {2}"
                                 .format(evaltype, type_, str_))

    def __call__(self, context):
        locals = dict(
            self = CEvalWrapper(context.GetDomainObject()),
            node = NodeEvalWrapper(context.GetDomainObject(), context.GetProjectNode()),
            cfg = CConfigEvalWrapper(),
            _line = context.GetLine(),
        )
        locals.update(context.GetVariables())
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

def BuildParam(value, domainType, localvars, type=None):
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
            return CParamEval(value[1:], domainType, localvars, type)
    elif type2 is not None:
        return type2(value)
    else:
        return value
