import re
from lib.Plugin.Interface import Reference
from lib.Plugin.Interface.meta import Meta

IDENTIFIER = 'UML.FRI'
FIRST_LINE_PLUGIN = re.compile(r'(?P<command>\w+) +(?P<type>[\w#:.]+) +%s/(?P<version>\d+\.\d+)\r?$' % IDENTIFIER)
FIRST_LINE_MAIN = re.compile(r'%s/(?P<version>\d+\.\d+) +(?P<code>\d{3})( (?P<text>[ \w]+))?\r?$' % IDENTIFIER)
PARAM_LINE = re.compile(r'(?P<key>[A-Za-z_]\w*): *(?P<value>[^\r\n]+)\r?$')
EMPTY_LINE = re.compile(r'(\r|\n|\r\n)$')

RESP_NOTIFY = 100
RESP_GUI_ACTIVATED = 101
RESP_DOMAIN_VALUE_CHANGED = 102

RESP_OK = 200
RESP_GUI_ADDED = 201
RESP_GUI_SENSITIVE = 202
RESP_GUI_INSENSITIVE = 203
RESP_METAMODEL_DESCRIPTION = 204
RESP_RESULT = 205

RESP_UNKONWN_COMMAND = 400
RESP_UNSUPPORTED_VERSION = 401
RESP_INVALID_COMMAND_TYPE = 402
RESP_MISSING_PARAMETER = 403
RESP_INVALID_PARAMETER = 404
RESP_INVALID_OBJECT = 405
RESP_UNKNOWN_METHOD = 406
RESP_PROJECT_NOT_LOADED = 407
RESP_UNKNOWN_CONSTRUCTOR = 408

RESP_UNHANDELED_EXCEPTION = 500

def t_2intTuple(val):
    try:
        assert len(x) > 4 and x[0] == '(' and x[-1] == ')'
        result = tuple(int(i)for i in x[1:-1].split(','))
        assert len(result) == 2
        return result
    except (AssertionError, ):
        raise ValueError()

def t_object(val):
    print `val`
    if val == 'project':
        return Reference.GetProject()
    elif re.match(r'#[0-9]+$', val) is not None:
        return Reference.GetObject(int(val[1:]))
    elif val == 'None':
        return None
    else:
        match = re.match(r'[ ]*(?P<clsname>[a-zA-Z][a-zA-Z0-9_]+)[(](?P<params>.*)[)][ ]*$', val)
        if match is not None and Meta.HasConstructor(match.groupdict()['clsname']):
            paramstr = match.groupdict()['params']
            braces = {'(': 0, '[': 0, '{': 0}
            reverse = {')':'(', ']':'[', '}':'{'}
            splits = [-1]
            for i, c in enumerate(paramstr):
                if c == ',' and all(j == 0 for j in braces.itervalues()):
                    splits.append(i)
                elif c in braces:
                    braces[c] += 1
                elif c in reverse:
                    braces[reverse[c]] -= 1
            splits.append(len(paramstr))
            params = []
            for i in xrange(1, len(splits)):
                params.append(paramstr[splits[i - 1] + 1 : splits[i]])
            return Meta.Create(match.groupdict()['clsname'], params)
        else:
            raise ValueError()

def t_classobject(cls):
    def check(val):
        res = t_object(val)
        if isinstance(res, cls):
            return res
        else:
            print res, cls
            raise ValueError()
    return check

def t_bool(val):
    if val == 'True':
        return True
    elif val == 'False':
        return False
    else:
        raise ValueError()

def t_elementType(val):
    try:
        f = Reference.GetProject().GetMetamodel().GetElementFactory()
        if f.HasType(val):
            return f.GetElement(val)
        else:
            raise ValueError()
    except AttributeError:
        raise ValueError()
    

def r_object(val):
    return '#%i' % (val.GetPluginId(), ) if val is not None else 'None'

def r_objectlist(val):
    return `list(r_object(i) for i in val)`

def r_bool(val):
    return str(bool(val))


