class params:
    def __init__(self, *types):
        self.__types = types
    
    def __call__(self, fnc):
        fnc.method_param_types = self.__types
        return fnc

def mainthread(fnc):
    fnc.method_in_mainthread = True
    return fnc

def polymorphic(fnc):
    fnc.method_polymorfic = True
    return fnc
