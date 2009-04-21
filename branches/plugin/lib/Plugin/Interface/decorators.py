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
            
