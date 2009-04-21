import re

class Meta(type):
    
    interface = {}
    reserved = re.compile(r'__[a-zA-Z0-9_]+__$')
    
    def __init__(self, name, bases, dictionary):
        type.__init__(self, name, bases, dictionary)
        self.interface[dictionary['__cls__']] = dict(
            (('__class__', self),) +
            tuple((fname, 
                {'params': dictionary[fname]._params if hasattr(dictionary[fname], '_params') else {},
                 'result': dictionary[fname]._result if hasattr(dictionary[fname], '_result') else lambda x: x})
            for fname in dictionary.iterkeys()
            if not self.reserved.match(fname)))
        for fname, fun in dictionary.iteritems():
            if not self.reserved.match(fname):
                setattr(self, fname, staticmethod(fun))
            
    @classmethod
    def GetMethod(self, cls, fname):
        cls = self.interface.get(cls)
        if cls and fname in cls:
            return (getattr(cls['__class__'], fname), cls[fname])
        else:
            return None
            
            
    