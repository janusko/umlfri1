from ..PluginBase import params, mainthread, polymorphic

from .Button import IButton

class IToggleButton(IButton):
    def __init__(self, button):
        IButton.__init__(button)
        
        self.__button = button
    
    def GetActive(self): 
        return self.__button.GetActive()
    
    @mainthread
    @params(bool)
    def SetActive(self, value):
        self.__button.SetActive(value)
