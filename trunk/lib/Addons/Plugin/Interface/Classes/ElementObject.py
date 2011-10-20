from DomainObject import IDomainObject
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.Classes.base import IBase
from lib.Addons.Plugin.Interface.decorators import *
from lib.Commands.Diagram import CCreateDiagramCommand
from lib.Drawing.Diagram import CDiagram
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Domains.Object import CDomainObject
from lib.Exceptions import *
from lib.Project import CProjectNode

class IElementObject(IDomainObject):
    __cls__ = CElementObject
    
    def GetName(him):
        return him.GetName()
    
    def GetDiagrams(him):
        node = him.GetNode()
        if node is not None:
            return node.GetDiagrams()
    
    def GetConnections(him):
        return list(him.GetConnections())
        
    def GetChildren(him):
        node = him.GetNode()
        if node is not None:
            return [n.GetObject() for n in node.GetChilds()]
        
    def GetAppears(him):
        return list(him.GetAppears())
    
    @destructive
    def ConnectWith(him, command, other, connectionType):
        connectionObject = CConnectionObject(connectionType, him, other)
        
        IBase.adapter.plugin_change_object(connectionObject)
    
    @destructive
    def CreateDiagram(him, command, diagramType):
        cmd = CCreateDiagramCommand(diagramType, him.GetNode())
        command.Execute(cmd)
        return cmd.GetDiagram()
    
    def CreateChildElement(him, elementType):
        parentNode = him.GetNode()
        
        elementObject = CElementObject(elementType)

        elementNode = CProjectNode(parentNode, elementObject)
        parentNode.AddChild(elementNode)
        
        IBase.adapter.plugin_change_object(elementObject)
    
    def ShowIn(him, diagram):
        if diagram.HasElement(him):
            raise PluginInvalidMethodParameters(him.GetUID(), "element is already shown on given diagram")
        
        elementVisual = CElement(diagram, him)
        
        IBase.adapter.plugin_change_visual(elementVisual)
