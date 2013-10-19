from ..PluginBase import params, mainthread, polymorphic

from .MenuItem import IMenuItem

class ICheckMenuItem(IMenuItem):
    def __init__(self, plugin, menuItem):
        IMenuItem.__init__(self, plugin, menuItem)
        
        self.__menuItem = menuItem

    def GetActive(self):
        return self.__menuItem.GetActive()
        
    @mainthread
    @params(bool)
    def SetActive(self, value):
        self.__menuItem.SetActive(value)
    
    def GetInconsistent(self):
        return self.__menuItem.GetInconsistent()
        
    @mainthread
    @params(bool)
    def SetInconsistent(self, value):
        self.__menuItem.SetInconsistent(value)
    
    def GetRadio(self):
        return self.__menuItem.GetRadio()
        
    @mainthread
    @params(bool)
    def SetRadio(self, value):
        self.__menuItem.SetRadio(value)
