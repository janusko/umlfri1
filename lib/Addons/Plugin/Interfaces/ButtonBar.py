from .Decorators import params, mainthread, polymorphic

from lib.GenericGui import CSeparator, CToggleButton, CButton

from . import Separator
from . import Button
from . import ToggleButton

class IButtonBar(object):
    def __init__(self, plugin, buttonBar):
        self.__plugin = plugin
        self.__buttonBar = buttonBar
    
    @property
    def uid(self):
        return self.__buttonBar.GetUID()
    
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
    @params(str, int, str, str)
    def AddButton(self, guiId, position, label, imageFileName):
        if imageFileName is not None:
            imageFileName = self.__plugin.RelativePath2Absolute(imageFileName)
        
        button = self.__buttonBar.AddButton(guiId, position, label, imageFileName, False, self.__plugin)
        return Button.IButton(self.__plugin, button)
    
    @mainthread
    @params(str, int, str, str)
    def AddToggleButton(self, guiId, position, label, imageFileName):
        if imageFileName is not None:
            imageFileName = self.__plugin.RelativePath2Absolute(imageFileName)
        
        button = self.AddButton(guiId, position, label, imageFileName, True, self.__plugin)
        return ToggleButton.IToggleButton(self.__plugin, button)
    
    @mainthread
    @params(str, int)
    def AddSeparator(self, guiId, position):
        return Separator.ISeparator(self.__buttonBar.AddSeparator(guiId, position, self.__plugin))
