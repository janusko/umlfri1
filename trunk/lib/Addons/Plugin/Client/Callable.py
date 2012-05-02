from lib.Addons.Plugin.Communication.Encoding import *

class CCallable(object):
    
    def __init__(self, id, fname, connection):
        self.id = id
        self.fname = fname
        self.connection = connection
    
    def __call__(self, *args, **kwds):
        args = tuple(EncodeValue(i, False, self.connection) for i in args)
        kwds = dict((k, EncodeValue(v, False, self.connection)) for k, v in kwds.iteritems())
        
        result = t_eval(self.connection.Execute('exec', '%s.%s'%(self.id, self.fname), args, kwds)())
        return DecodeValue(result, False, self.connection)
    