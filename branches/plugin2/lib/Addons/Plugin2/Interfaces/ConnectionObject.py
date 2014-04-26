from .Decorators import params, mainthread, polymorphic

from lib.Commands.Diagrams import CShowConnectionCommand, ShowConnectionError
from lib.Connections import CConnectionAlias, CConnectionType
from lib.Exceptions import PluginInvalidMethodParameters

from .DomainObject import IDomainObject

from . import ConnectionAlias
from . import ConnectionType
from . import ConnectionVisual

class IConnectionObject(IDomainObject):
    def __init__(self, plugin, connection):
        IDomainObject.__init__(self, plugin, connection)
        
        self.__connection = connection
        self.__plugin = plugin
    
    @property
    def uid(self):
        return self.__connection.GetUID()
    
    @property
    def _connection(self):
        return self.__connection
    
    @params(object)
    def GetConnectedObject(self, obj):
        from . import ElementObject
        
        return ElementObject.IElementObject(self.__plugin, self.__connection.GetConnectedObject(obj._element))
    
    @polymorphic
    def GetType(self):
        type = self.__connection.GetType()
        if isinstance(type, CConnectionAlias):
            return ConnectionAlias.IConnectionAlias(type)
        elif isinstance(type, CConnectionType):
            return ConnectionType.IConnectionAlias(type)

    def GetDestination(self):
        from . import ElementObject
        
        return ElementObject.IElementObject(self.__plugin, self.__connection.GetDestination())
    
    def GetSource(self):
        from . import ElementObject
        
        return ElementObject.IElementObject(self.__plugin, self.__connection.GetSource())
    
    def GetAppears(self):
        from . import Diagram
        
        for diagram in self.__connection.GetAppears():
            yield Diagram.IDiagram(self.__plugin, diagram)

    @params(object)
    def ShowIn(self, diagram):
        if diagram.HasConnection(self.__connection):
            raise PluginInvalidMethodParameters(self.__connection.GetUID(), "connection is already shown on given diagram")
        
        try:
            cmd = CShowConnectionCommand(self.__connection, diagram._diagram)
            self.__plugin.GetTransaction().Execute(cmd)
        except ShowConnectionError, e:
            raise PluginInvalidMethodParameters(self.__connection.GetUID(), str(e))
        
        return ConnectionVisual.IConnectionVisual(self.__plugin, cmd.GetConnectionVisual())
