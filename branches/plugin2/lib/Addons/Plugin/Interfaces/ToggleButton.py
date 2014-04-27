from .Decorators import params, mainthread, polymorphic

from .Button import IButton

class IToggleButton(IButton):
    def __init__(self, plugin, button):
        IButton.__init__(plugin, button)
        
        self.__button = button
    
    @property
    def uid(self):
        return self.__button.GetUID()
    
    def GetActive(self): 
        return self.__button.GetActive()
    
    @mainthread
    @params(bool)
    def SetActive(self, value):
        self.__button.SetActive(value)
