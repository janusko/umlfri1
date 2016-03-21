from DomainObject import IDomainObject
from lib.Addons.Plugin.Interface.Classes.base import IBase
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Commands.Diagrams import CShowConnectionCommand, ShowConnectionError
from lib.Connections import CConnectionObject
from lib.Drawing.Connection import CConnection
from lib.Elements import CElementObject

class IConnectionObject(IDomainObject):
    __cls__ = CConnectionObject
    
    def GetConnectedObject(him, obj):
        return him.GetConnectedObject(obj)
        
    def GetDestination(him):
        return him.GetDestination()
    
    def GetSource(him):
        return him.GetSource()
    
    def GetAppears(him):
        return list(him.GetAppears())
    
    @destructive
    def ShowIn(him, command, diagram):
        if diagram.HasConnection(him):
            raise PluginInvalidMethodParameters(him.GetUID(), "connection is already shown on given diagram")
        
        try:
            cmd = CShowConnectionCommand(him, diagram)
            command.Execute(cmd)
        except ShowConnectionError, e:
            raise PluginInvalidMethodParameters(him.GetUID(), str(e))
        
        return cmd.GetConnectionVisual()
