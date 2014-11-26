from .Decorators import params, mainthread, polymorphic

from .Widget import IWidget

class IButton(IWidget):
    def __init__(self, button):
        IWidget.__init__(self, button)
        
        self.__button = button
    
    @property
    def uid(self):
        return self.__button.GetUID()

    def GetLabel(self):
        return self.__button.GetLabel()
    
    @mainthread
    @params(bool)
    def SetLabel(self, value):
        self.__button.SetLabel(value)
