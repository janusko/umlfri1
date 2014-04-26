from .Decorators import params, mainthread, polymorphic

from .VisibleObject import IVisibleObject

from lib.Commands.Diagrams import CCreateConnectionCommand
from lib.Exceptions import PluginInvalidMethodParameters

from . import ConnectionVisual


class IElementVisual(IVisibleObject):
    def __init__(self, plugin, element):
        IVisibleObject.__init__(self, plugin, element)
        
        self.__plugin = plugin
        self.__element = element
    
    @property
    def uid(self):
        return self.__element.GetUID()
    
    def GetConnections(self):
        for connection in self.__element.GetConnections():
            yield ConnectionVisual.IConnectionVisual(self.__plugin, connection)
    
    @params(object, object)
    def ConnectWith(self, other, connectionType):
        diagram = self.__element.GetDiagram()
        if diagram is not other.__element.GetDiagram():
            raise PluginInvalidMethodParameters(self.__element.GetUID(), 'Elements must be on the same diagram')
        
        cmd = CCreateConnectionCommand(self.__element, other.__element, connectionType._elementType)
        self.__plugin.GetTransaction().Execute(cmd)
        return ConnectionVisual.IConnectionVisual(self.__plugin, cmd.GetConnectionVisual())
    
    def GetObject(self):
        from . import ElementObject
        
        return ElementObject.IElementObject(self.__plugin, self.__element.GetObject())
