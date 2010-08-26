def parameter(name, transform):
    def transformation(fun):
        if not hasattr(fun, '_params'):
            fun._params = {}
        fun._params[name] = transform
        return fun
    return transformation
        
def result(transform):
    def transformation(fun):
        fun._result = transform
        return fun
    return transformation
            

def not_interface(fun):
    fun._not_iterface = True
    return fun

def destructive(fun):
    fun._destructive = True
    return fun

def reverse(transform):
    def transformation(fun):
        fun._reverse = transform
        return fun
    return transformation
    
import gobject, thread, sys

class CSynchronized(object):
    
    def __init__(self, fun):
        self.fun = fun
        self.result = None
        self.exception = None
        self.lock = thread.allocate()
        self.lock.acquire()
    
    def __call__(self, *a, **k):
        gobject.idle_add(self.work, a, k)
        self.lock.acquire()
        if self.exception is None:
            return self.result
        else:
            raise self.exception[1], None, self.exception[2]
        
    def work(self, a, k):
        try:
            self.result = self.fun(*a, **k)
        except (Exception, ), e:
            self.exception = sys.exc_info()
        finally:
            self.lock.release()

def mainthread(fun):
    fun._synchronized = CSynchronized(fun)
    return fun