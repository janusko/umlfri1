from DomainObject import IDomainObject
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.Classes.base import IBase
from lib.Addons.Plugin.Interface.decorators import *
from lib.Drawing.Diagram import CDiagram
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
    def ConnectWith(him, other, connectionType):
        connectionObject = CConnectionObject(connectionType, him, other)
        
        IBase.adapter.plugin_change_object(connectionObject)
    
    @destructive
    def CreateDiagram(him, diagramType):
        diagram = CDiagram(diagramType)
        node = him.GetNode()
        node.AddDiagram(diagram)
        diagram.SetPath(node.GetPath() + "/" + diagram.GetName() + ":=Diagram=")
        
        IBase.adapter.plugin_diagram_created(diagram)
    
    def CreateChildElement(him, elementType):
        parentNode = him.GetNode()
        
        elementObject = CElementObject(elementType)

        elementNode = CProjectNode(parentNode, elementObject, parentNode.GetPath() + "/" + elementObject.GetName() + ":" + elementObject.GetType().GetId())
        parentNode.AddChild(elementNode)
        
        IBase.adapter.plugin_change_object(elementObject)
