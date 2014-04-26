from .Decorators import params, mainthread, polymorphic

from lib.GenericGui import CCheckMenuItem, CMenuItem, CSeparator

from . import MenuItem
from . import CheckMenuItem
from . import Separator

class IMenu(object):
    def __init__(self, plugin, menu):
        self.__plugin = plugin
        self.__menu = menu
    
    @property
    def uid(self):
        return self.__menu.GetUID()
    
    def __castItem(self, item):
        if isinstance(item, CCheckMenuItem):
            return CheckMenuItem.IMenuItem(self.__plugin, item)
        elif isinstance(item, CMenuItem):
            return MenuItem.IMenuItem(self.__plugin, item)
        elif isinstance(item, CSeparator):
            return Separator.ISeparator(item)
    
    @mainthread
    def AddMenuItem(self, guiId, callback, position, label, underline, imageFileName):
        if imageFileName is not None:
            imageFileName = self.__plugin.RelativePath2Absolute(imageFileName)
        return MenuItem.IMenuItem(self.__plugin, self.__menu.AddMenuItem(guiId, callback, position, label, underline, imageFileName, self.__plugin))
    
    @mainthread
    def AddCheckMenuItem(self, guiId, callback, position, label, underline):
        return CheckMenuItem.IMenuItem(self.__plugin, self.__menu.AddCheckMenuItem(guiId, callback, position, label, underline, self.__plugin))
    
    @mainthread
    def AddSeparator(self, guiId, position):
        return Separator.ISeparator(self.__menu.AddSeparator(guiId, position, self.__plugin))
    
    @polymorphic
    def GetItems(self):
        for item in self.__menu.GetItems():
            yield self.__castItem(item)
    
    @polymorphic
    def GetItem(self, guiId):
        return self.__castItem(self.__menu.GetItem(guiId))
