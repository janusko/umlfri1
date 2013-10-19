from .Decorators import params, mainthread, polymorphic

from lib.GenericGui import CSeparator, CToggleButton, CButton

from . import Separator
from . import Button
from . import ToggleButton

class IButtonBar(object):
    def __init__(self, plugin, buttonBar):
        self.__plugin = plugin
        self.__buttonBar = buttonBar
    
    def __castItem(self, item):
        if isinstance(item, CSeparator):
            return Separator.ISeparator(item)
        elif isinstance(item, CButton):
            return Button.IButton(item)
        elif isinstance(item, CToggleButton):
            return ToggleButton.IToggleButton(item)
        
    @polymorphic
    def GetItems(self):
        for item in self.__buttonBar.GetItems():
            yield self.__castItem(item)
    
    @polymorphic
    def GetItem(self, guiId):
        item = self.__buttonBar.GetItem(guiId)
        return self.__castItem(item)
    
    @mainthread
    @params(str, callable, int, str, str, bool)
    @polymorphic
    def AddButton(self, guiId, callback, position, label, imageFileName, toggleButton):
        if imageFileName is not None:
            imageFileName = self.__plugin.RelativePath2Absolute(imageFileName)
        
        button = self.__buttonBar.AddButton(guiId, callback, position, label, imageFileName, toggleButton, self.__plugin)
        return self.__castItem(button)
    
    @mainthread
    @params(str, int)
    def AddSeparator(self, guiId, position):
        return Separator.ISeparator(self.__buttonBar.AddSeparator(guiId, position, self.__plugin))
