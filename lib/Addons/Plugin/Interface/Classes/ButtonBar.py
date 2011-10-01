from Container import IContainer
from lib.GenericGui import CButtonBar
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *

class IButtonBar(IContainer):
    
    __cls__ = CButtonBar
    
    @mainthread
    @includeAddr
    def AddButton(him, guiId, callback, position, label, imageFileName=None, toggleButton=False, _addr=None):
        if imageFileName is not None:
            imageFileName = IButtonBar.RelativePath2Absolute(_addr, imageFileName)
        return him.AddButton(guiId, callback, position, label, imageFileName, toggleButton, _addr)
        
    @mainthread
    @includeAddr
    def AddSeparator(him, guiId, position, _addr=None):
        return him.AddSeparator(guiId, position, _addr)
