import re
from lib.Plugin.Interface import Reference

IDENTIFIER = 'UML.FRI'
FIRST_LINE_PLUGIN = re.compile(r'(?P<command>\w+) +(?P<type>[\w#:.]+) +%s/(?P<version>\d+\.\d+)\r?$' % IDENTIFIER)
FIRST_LINE_MAIN = re.compile(r'%s/(?P<version>\d+\.\d+) +(?P<code>\d{3})( (?P<text>[ \w]+))?\r?$' % IDENTIFIER)
PARAM_LINE = re.compile(r'(?P<key>[A-Za-z_]\w*): *(?P<value>[^\r\n]+)\r?$')
EMPTY_LINE = re.compile(r'(\r|\n|\r\n)$')

RESP_NOTIFY = 100
RESP_GUI_ACTIVATED = 101

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
    if re.match(r'#[0-9]+$', val) is not None:
        return Reference.GetObject(int(val[1:]))
    elif val == 'None':
        return None
    else:
        raise ValueError()

def t_classobject(cls):
    def check(val):
        res = t_object(val)
        if isinstance(val, cls):
            return res
        else:
            raise ValueError()
    return check

def r_object(val):
    return '#%i' % (val.GetPluginId(), ) if val is not None else 'None'

def r_objectlist(val):
    return `list(r_object(i) for i in val)`
