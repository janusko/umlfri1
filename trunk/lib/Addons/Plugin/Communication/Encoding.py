import ComSpec
from lib.Base import CBaseObject
from lib.Addons.Plugin.Client import classes

def rc_eval(*a):
    return ComSpec.rc_eval(*a)

def r_eval(*a):
    return ComSpec.r_eval(*a)

def EncodeValue(value, app, con = None, addr = None):
    fun = None
    if isinstance(value, bool):
        fun = 'bool'
    elif isinstance(value, (CBaseObject, ) + tuple(classes.values())):
        fun = 'object'
    elif app and isinstance(con.GetGuiManager().GetItem(value), CBaseObject):
        value = con.guimanager.GetItem(value)
        fun = 'object'
    elif isinstance(value, (str, unicode)):
        fun = 'str'
    elif isinstance(value, (int, long)):
        fun = 'int'
    elif isinstance(value, list) and (len(value) == 0 or isinstance(value[0], CBaseObject)):
        fun = 'objectlist'
    elif isinstance(value, tuple) and len(val) == 2:
        if isinstance(val[0], int):
            fun = '2intTuple'
        elif isinstance(val[0], bool):
            fun = '2boolTuple'
        elif isinstance(val[0], tuple):
            fun = '2x2intTuple'
    elif callable(value):
        fun = 'callback'
    elif value is None:
        fun = 'none'
    else:
        try:
            if value == rc_eval(r_eval(value, con, addr), con, addr):
                fun = 'eval'
        except:
            pass
    
    if fun is not None:
        if app:
            ff = getattr(ComSpec, 'r_' + fun)
        else:
            ff = getattr(ComSpec, 't_' + fun)._reverse
    else:
        raise ValueError
    
    return fun, ff(value, con, addr)
    
def DecodeValue(value, app, con = None, addr = None):
    if app:
        fun = getattr(ComSpec, 't_' + value[0])
    else:
        fun = getattr(ComSpec, 'r_' + value[0])._reverse
    
    return fun(value[1], con, addr)
    
