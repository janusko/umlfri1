from VisibleObject import IVisibleObject
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.Classes.base import IBase
from lib.Addons.Plugin.Interface.decorators import *
from lib.Connections.Object import CConnectionObject
from lib.Drawing.Connection import CConnection
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Drawing.Diagram import CDiagram

class IElementVisual(IVisibleObject):
    __cls__ = CElement
    
    def GetConnections(him):
        return list(him.GetConnections())
    
    @destructive
    def ConnectWith(him, command, other, connectionType):
        diagram = him.GetDiagram()
        if diagram is not other.GetDiagram():
            raise PluginInvalidMethodParameters(him.GetUID(), 'Elements must be on the same diagram')
        connectionObject = CConnectionObject(connectionType, him.GetObject(), other.GetObject())
        connectionVisual = CConnection(diagram, connectionObject, him, other)
        
        IBase.adapter.plugin_change_object(connectionVisual)
        IBase.adapter.plugin_change_visual(connectionVisual)
