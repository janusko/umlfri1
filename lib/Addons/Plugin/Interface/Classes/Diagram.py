from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Commands.Diagrams import CCreateElementCommand
from lib.Drawing.Connection import CConnection
from lib.Drawing.Diagram import CDiagram
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Addons.Plugin.Interface.Classes.DomainObject import IDomainObject
from lib.Drawing import CConLabelInfo
from lib.Project.ProjectNode import CProjectNode

class IDiagram(IDomainObject):
    __cls__ = CDiagram
    
    def GetElement(him, obj):
        return him.HasElementObject(obj)
    
    def GetConnection(him, obj):
        return him.GetConnection(obj)
    
    def GetSelected(him):
        return list(IBase.GetAdapter().application.GetOpenedDrawingAreas().GetDrawingArea(him).GetSelection().GetSelected())

    def GetSelectedElements(him):
        return list(IBase.GetAdapter().application.GetOpenedDrawingAreas().GetDrawingArea(him).GetSelection().GetSelectedElements(True))

    def GetSelectedConnectionLabels(him):
        selElements = IBase.GetAdapter().application.GetOpenedDrawingAreas().GetDrawingArea(him).GetSelection().GetSelectedElements(False)
        return [item for item in selElements if isinstance(item, CConLabelInfo)]
    
    def GetSelectedConnections(him): 
        return list(IBase.GetAdapter().application.GetOpenedDrawingAreas().GetDrawingArea(him).GetSelection().GetSelectedConnections())
        
    def GetSelectSquare(him):
        selection = IBase.GetAdapter().application.GetOpenedDrawingAreas().GetDrawingArea(him).GetSelection()
        return him.GetSelectSquare(selection)
    
    def GetElementAtPosition(him, pos): 
        return him.GetElementAtPosition(pos)
    
    def GetElementsInRange(him, topLeft, bottomRight, includeAll = True):
        return list(him.GetElementsInRange(topLeft, bottomRight, includeAll))
    
    def GetSizeSquare(him):
        return him.GetSizeSquare()
    
    def GetElements(him):
        return list(him.GetElements())
        
    def GetConnections(him):
        return list(him.GetConnections())
    
    def GetName(him):
        return him.GetName()
    
    @destructive
    def CreateElement(him, command, elementType):
        cmd = CCreateElementCommand(elementType, him, IBase.GetAdapter().application.GetOpenedDrawingAreas())
        command.Execute(cmd)
        return cmd.GetElementVisual()
