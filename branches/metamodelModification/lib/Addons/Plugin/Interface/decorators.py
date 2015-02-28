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
            r = self.result
            self.result = None
            return r
        else:
            e = self.exception
            self.exception = None
            raise e[1], None, e[2]
        
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
    
def includeAddr(fun):
    fun._include_addr = True
    return fun
