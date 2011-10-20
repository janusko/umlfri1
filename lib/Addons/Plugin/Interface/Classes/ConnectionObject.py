from DomainObject import IDomainObject
from lib.Addons.Plugin.Interface.Classes.base import IBase
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Plugin.Communication.ComSpec import *
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
        
        source = diagram.GetElement(him.GetSource())
        destination = diagram.GetElement(him.GetDestination())
        
        if source is None or destination is None:
            raise PluginInvalidMethodParameters(him.GetUID(), "source and destination must be present on the given diagram")
        connectionVisual = CConnection(diagram, him, source, destination)
        
        IBase.adapter.plugin_change_visual(connectionVisual)
