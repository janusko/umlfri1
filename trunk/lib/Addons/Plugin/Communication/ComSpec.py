import re
import base64
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Interface.meta import Meta
from lib.Addons.Plugin.Client import classes
from lib.Base.Registrar import registrar

IDENTIFIER = 'UML.FRI'
VERSION = '0.1'
FIRST_LINE_PLUGIN = re.compile(r'(?P<command>\w+) +(?P<type>[-#0-9a-zA-Z_:.]+) +%s/(?P<version>\d+\.\d+)\r?$' % IDENTIFIER)
FIRST_LINE_MAIN = re.compile(r'%s/(?P<version>\d+\.\d+) +(?P<code>\d{3})( (?P<text>[ \w]+))?\r?$' % IDENTIFIER)
PARAM_LINE = re.compile(r'(?P<key>[A-Za-z_]\w*): *(?P<value>[^\r\n]+)\r?$')
EMPTY_LINE = re.compile(r'(\r|\n|\r\n)$')

RESP_NOTIFY = 100
RESP_GUI_ACTIVATED = 101
RESP_DOMAIN_VALUE_CHANGED = 102
RESP_FINALIZE = 103
RESP_CALLBACK = 104


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
RESP_TRANSACTION_PENDING = 409
RESP_OUT_OF_TRANSACTION = 410
RESP_TRANSACTION_MODE_UNSPECIFIED = 411
RESP_INVALID_METHOD_PARAMETER = 412

RESP_UNHANDELED_EXCEPTION = 500

def tc_object(val, conn = None, addr = None):
    return val.GetId()

def t_2intTuple(x, conn = None, addr = None):
    try:
        assert len(x) > 4 and x[0] == '(' and x[-1] == ')'
        result = tuple(int(i)for i in x[1:-1].split(','))
        assert len(result) == 2
        return result
    except (AssertionError, ):
        raise ValueError()
        
def t_bool(val, conn = None, addr = None):
    if val == 'True':
        return True
    elif val == 'False':
        return False
    else:
        raise ValueError()
        
def t_2boolTuple(x, conn = None, addr = None):
    if not (len(x) > 4 and x[0] == '(' and x[-1] == ')'):
        raise ValueError()
    result = tuple(t_bool(i.strip()) for i in x[1:-1].split(','))
    if len(result) != 2:
        raise ValueError()
    return result

@reverse(tc_object)
def t_object(val, conn = None, addr = None):
    if val == 'None':
        return None
    elif re.match(r'#[-0-9a-z]+$', val) is not None:
        return registrar.GetObject(val[1:])
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
    def check(val, conn = None, addr = None):
        res = t_object(val)
        if isinstance(res, cls):
            return res
        else:
            raise ValueError()
    check = reverse(tc_object)(check)
    return check

def t_2x2intTuple(val, conn = None, addr = None):
    match = re.match(r'\(\((?P<a>[0-9]+),(?P<b>[0-9]+)\),\((?P<c>[0-9]+),(?P<d>[0-9]+)\)\)$', val)
    if match is not None:
        d = match.groupdict()
        return ((int(d['a']), int(d['b'])), (int(d['c']), int(d['d'])))
    else:
        raise ValueError()

def rc_object(val, connection, addr = None):
    if val.find('::') >= 0:
        val, cls = val.split('::')
        if val == 'None':
            return None
        else:
            try:
                return classes[cls](val, connection)
            except KeyError:
                raise ValueError()
    else:
        raise ValueError()
    
def rc_objectlist(val, connection, addr = None):
    return [rc_object(i, connection) for i in val[1:-1].split(',') if i != '']
    

@reverse(rc_object)
def r_object(val, conn = None, addr = None):
    return ('#%s::%s' % (val.GetUID(), Meta.GetClassName(val)) if val is not None else 'None::NoneType') 
        

@reverse(rc_objectlist)
def r_objectlist(val, conn = None):
    return '[' + ','.join(r_object(i) for i in val) + ']'

@reverse(t_bool)
def r_bool(val, conn = None, addr = None):
    return str(bool(val))

t_bool = reverse(r_bool)(t_bool)

@reverse(t_2intTuple)
def r_2intTuple(val, conn = None, addr = None):
    assert type(val) == tuple and len(val) == 2 and all(type(i) == int for i in val)
    return '(%i,%i)' % val
    
t_2intTuple = reverse(r_2intTuple)(t_2intTuple)

@reverse(t_2boolTuple)
def r_2boolTuple(val, conn = None, addr = None):
    if type(val) != tuple or len(val) != 2 or any(type(i) != bool for i in val):
        raise ValueError()
    return str(val)

t_2boolTuple = reverse(r_2boolTuple)(t_2boolTuple)

@reverse(t_2x2intTuple)
def r_2x2intTuple(val, conn = None, addr = None):
    return '((%i,%i),(%i,%i))' % (val[0] + val[1])

t_2x2intTuple = reverse(r_2x2intTuple)(t_2x2intTuple)

@reverse(lambda val, conn = None: None)
def r_none(val, conn = None, addr = None):
    if val is None:
        return 'None'
    else:
        raise ValueError()

def rc_eval(val, con=None, addr = None):
    return eval(val, {}, {'__builtins__': {}})
    
@reverse(rc_eval)
def r_eval(val, con=None, addr = None):
    return str(val)

def t_str(val, con = None, addr = None):
    try:
        if val == 'None':
            return None
        else:
            val = base64.b64decode(val)
            if val[-1] == '\0':
                return val[:-1]
            elif val[-1] == '\x01':
                return unicode(val[:-1])
            else:
                raise ValueError()
    except TypeError:
        raise ValueError()
        
@reverse(t_str)
def r_str(val, con=None, addr = None):
    if val is None:
        return 'None'
    elif isinstance(val, str):
        return base64.b64encode(val + '\0')
    elif isinstance(val, unicode):
        return base64.b64encode(val + '\x01')
    else:
        raise ValueError()
    
t_str = reverse(r_str)(t_str)

def tc_callback(val, con = None, addr = None):
    if val is None:
        result = 'None'
    else:
        result = str(con.SetCallback(val))
    return result

@reverse(tc_callback)
def t_callback(val, con = None, addr = None):
    if val == 'None':
        return None
    else:
        result = lambda *a, **kw: con._callback(val, addr, **kw)
        result._callbackId = (val, addr)
        return result
    

def r_int(val, con = None, addr = None):
    if isinstance(val, (int, long)):
        return str(val)
    else:
        raise ValueError()

@reverse(r_int)
def t_int(val, con = None, addr = None):
    return int(val)
    
r_int = reverse(t_int)(r_int)
    