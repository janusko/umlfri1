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
    