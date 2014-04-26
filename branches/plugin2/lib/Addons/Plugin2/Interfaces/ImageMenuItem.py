from .Decorators import params, mainthread, polymorphic

from .MenuItem import IMenuItem

class IImageMenuItem(IMenuItem):
    def __init__(self, plugin, menuItem):
        IMenuItem.__init__(self, plugin, menuItem)
        
        self.__plugin = plugin
        self.__menuItem = menuItem
    
    @property
    def uid(self):
        return self.__menuItem.GetUID()
    
    @mainthread
    @params(str)
    def SetImageFromFile(self, filename):
        if filename is not None:
            filename = self.__plugin.RelativePath2Absolute(filename)
        self.__menuItem.SetImageFromFile(filename)
