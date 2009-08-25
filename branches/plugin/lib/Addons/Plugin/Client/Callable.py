class CCallable(object):
    
    def __init__(self, id, fname, fun, desc, connection):
        self.id = id
        self.fname = fname
        self.fun = fun
        self.desc = desc
        self.connection = connection
    
    def __call__(self, *args, **params):
        params.update(zip(self.fun.func_code.co_varnames[1:self.fun.func_code.co_argcount], args))
        params = dict((key, self.desc['params'][key]._reverse(params[key])) for key in params)
        return self.desc['result']._reverse(self.connection.Execute('exec', '%s.%s'%(self.id, self.fname), params)(), self.connection)
    