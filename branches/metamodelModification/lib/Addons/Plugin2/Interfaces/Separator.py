from .Decorators import params, mainthread, polymorphic

from .Widget import IWidget

class ISeparator(IWidget):
    def __init__(self, separator):
        IWidget.__init__(self, separator)
        
        self.__separator = separator
    
    @property
    def uid(self):
        return self.__separator.GetUID()
