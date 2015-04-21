from ..Base.Command import CCommand
from lib.Connections.Object import CConnectionObject
from lib.Drawing.Connection import CConnection

class CCreateConnectionCommand(CCommand):
    def __init__(self, sourceElement, destinationElement, connectionType, openedDrawingAreas):
        CCommand.__init__(self)
        
        self.__sourceElement = sourceElement
        self.__destinationElement = destinationElement
        self.__connectionType = connectionType
        self.__openedDrawingAreas = openedDrawingAreas
        self.__diagram = None
        self.__connectionObject = None
        self.__connectionVisual = None
    
    def _Do(self):
        self.__diagram = self.__sourceElement.GetDiagram()
        self.__connectionObject = CConnectionObject(
            self.__connectionType,
            self.__sourceElement.GetObject(),
            self.__destinationElement.GetObject()
        )
        self.__connectionVisual = CConnection(
            self.__diagram,
            self.__connectionObject,
            self.__sourceElement,
            self.__destinationElement
        )
    
    def _Redo(self):
        self.__sourceElement.GetObject().AddConnection(self.__connectionObject)
        self.__destinationElement.GetObject().AddConnection(self.__connectionObject)
        
        self.__diagram.AddConnection(self.__connectionVisual)
    
    def _Undo(self):
        self.__sourceElement.GetObject().RemoveConnection(self.__connectionObject)
        self.__destinationElement.GetObject().RemoveConnection(self.__connectionObject)
        
        self.__diagram.DeleteConnection(self.__connectionVisual, self.__openedDrawingAreas.GetDrawingArea(self.__diagram).GetSelection())
    
    def GetGuiUpdates(self):
        return [
            ('createConnectionObject', self.__connectionObject),
            ('connectionChanged', (self.__connectionVisual, []))
        ]
    
    def __str__(self):
        return _("Connection created between objects %s and %s on the diagram %s") % (
            self.__sourceElement.GetObject().GetName(),
            self.__destinationElement.GetObject().GetName(),
            self.__diagram.GetName()
        )
    
    def GetConnectionVisual(self):
        return self.__connectionVisual
    
    def GetConnectionObject(self):
        return self.__connectionObject
