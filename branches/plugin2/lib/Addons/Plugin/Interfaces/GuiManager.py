from .Decorators import params, mainthread, polymorphic

from . import ButtonBar
from . import Menu


class IGuiManager(object):
    def __init__(self, plugin, guiManager):
        self.__plugin = plugin
        self.__manager = guiManager
    
    @property
    def uid(self):
        return self.__manager.GetUID()
    
    def GetMainMenu(self):
        return Menu.IMenu(self.__plugin, self.__manager.GetMainMenu())
        
    def GetTabMenu(self):
        return Menu.IMenu(self.__plugin, self.__manager.GetTabMenu())
        
    def GetTreeMenu(self):
        return Menu.IMenu(self.__plugin, self.__manager.GetTreeMenu())
    
    def GetDrawMenu(self):
        return Menu.IMenu(self.__plugin, self.__manager.GetDrawMenu())
    
    def GetButtonBar(self):
        return ButtonBar.IButtonBar(self.__plugin, self.__manager.GetButtonBar())
    
    def DisplayWarning(self, text):
        self.__manager.DisplayWarning(text)
        
    @mainthread
    def DeleteMe(self):
        self.__manager.DisposeOf(self.__plugin)
    
    @mainthread
    def HideMe(self):
        self.__manager.Hide(self.__plugin)
    
    @mainthread
    def ShowMe(self):
        self.__manager.Show(self.__plugin)
