import ComSpec
from lib.Base import CBaseObject

def t_eval(*a):
    return ComSpec.t_eval(*a)

def r_eval(*a):
    return ComSpec.r_eval(*a)

def EncodeValue(value, con = None, addr = None):
    fun = None
    if isinstance(value, bool):
        fun = 'bool'
    elif isinstance(value, CBaseObject):
        fun = 'object'
    elif isinstance(con.GetGuiManager().GetItem(value), CBaseObject):
        value = con.guimanager.GetItem(value)
        fun = 'object'
    elif isinstance(value, (str, unicode)):
        fun = 'str'
    elif isinstance(value, (int, long)):
        fun = 'int'
    elif isinstance(value, list) and (len(value) == 0 or isinstance(value[0], CBaseObject)):
        fun = 'objectlist'
    elif callable(value):
        fun = 'callback'
    elif value is None:
        fun = 'none'
    else:
        try:
            if value == t_eval(r_eval(value, con, addr), con, addr):
                fun = 'eval'
        except:
            pass
    
    if fun is not None:
        ff = getattr(ComSpec, 'r_' + fun)
    else:
        raise ValueError
    
    return fun, ff(value, con, addr)
    
def DecodeValue(value, con = None, addr = None):
    fun = getattr(ComSpec, 't_' + value[0])
    
    return fun(value[1], con, addr)
    
