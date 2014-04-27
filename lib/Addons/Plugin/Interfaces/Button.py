from .Decorators import params, mainthread, polymorphic

from .Widget import IWidget

class IButton(IWidget):
    def __init__(self, plugin, button):
        IWidget.__init__(self, button)
        
        self.__plugin = plugin
        self.__button = button
    
    @property
    def uid(self):
        return self.__button.GetUID()

    def GetLabel(self):
        return self.__button.GetLabel()
    
    @mainthread
    @params(bool)
    def SetLabel(self, value):
        self.__button.SetLabel(value)
    
    def AttachClicked(self):
        self.__button.ConnectClicked(self.__clickedHandler)
    
    def DetachClicked(self):
        self.__button.DisconnectClicked(self.__clickedHandler)
    
    def __clickedHandler(self):
        self.__plugin.FireEvent(self, 'Clicked')
