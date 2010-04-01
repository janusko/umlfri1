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

def factory(fun):
    fun._constructor = True
    fun._result = lambda x: x
    fun._destructive = True
    return fun
    

def reverse(transform):
    def transformation(fun):
        fun._reverse = transform
        return fun
    return transformation
    
import gobject, thread

class CSynchronized(object):
    
    def __init__(self, fun):
        self.fun = fun
        self.result = None
        self.lock = thread.allocate()
        self.lock.acquire()
    
    def __call__(self, *a, **k):
        gobject.idle_add(self.work, a, k)
        self.lock.acquire()
        return self.result
        
    def work(self, a, k):
        self.result = self.fun(*a, **k)
        self.lock.release()

def mainthread(fun):
    fun._synchronized = CSynchronized(fun)
    return fun