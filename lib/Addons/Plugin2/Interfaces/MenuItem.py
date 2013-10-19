from ..PluginBase import params, mainthread, polymorphic

from .Widget import IWidget

class IMenuItem(IWidget):
    def __init__(self, plugin, menuItem):
        IWidget.__init__(menuItem)
        
        self.__plugin = plugin
        self.__menuItem = menuItem
    
    def GetSubmenu(self):
        return self.__menuItem.GetSubmenu()
        
    def GetLabel(self):
        return self.__menuItem.GetLabel()
        
    @mainthread
    @params(str)
    def SetLabel(self, value):
        self.__menuItem.SetLabel(value)
        
    @mainthread
    def AddSubmenu(self):
        return self.__menuItem.AddSubmenu(self.__plugin)
