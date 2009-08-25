class CExceptionCarrier(object):
    
    def __init__(self, ecls, *args, **kwds):
        self.ecls = ecls
        self.args = args
        self.kwds = kwds
    
    def throw(self):
        raise self.ecls(*self.args, **self.kwds)
