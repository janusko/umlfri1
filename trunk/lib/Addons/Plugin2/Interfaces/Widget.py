from ..PluginBase import params, mainthread, polymorphic

class IWidget(object):
    def __init__(self, widget):
        self.__widget = widget
    
    def GetGuiId(self):
        return self.__widget.GetGuiId()
    
    @mainthread
    @params(bool)
    def SetEnabled(self, value):
        self.__widget.SetSensitive(value)
    
    def GetEnabled(self):
        return self.__widget.GetSensitive()
    
    def GetVisible(self):
        return self.__widget.GetVisible()
        
    @mainthread
    @params(bool)
    def SetVisible(self, value):
        self.__widget.SetVisible(value)
