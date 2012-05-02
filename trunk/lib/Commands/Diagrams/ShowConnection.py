from ..Base.Command import CCommand
from lib.Drawing import CConnection

class ShowConnectionError(Exception):
    pass

class CShowConnectionCommand(CCommand):
    def __init__(self, connectionObject, diagram):
        CCommand.__init__(self)
        
        self.__connectionObject = connectionObject
        self.__diagram = diagram
        self.__connectionVisual = None
    
    def _Do(self):
        source = self.__diagram.GetElement(self.__connectionObject.GetSource())
        destination = self.__diagram.GetElement(self.__connectionObject.GetDestination())
        
        if source is None or destination is None:
            raise ShowConnectionError("source and destination must be present on the given diagram")
        
        self.__connectionVisual = CConnection(self.__diagram, self.__connectionObject, source, destination)
    
    def _Redo(self):
        self.__diagram.AddConnection(self.__connectionVisual)
    
    def _Undo(self):
        self.__diagram.DeleteConnection(self.__connectionVisual)
    
    def GetGuiUpdates(self):
        return [
            ('connectionChanged', (self.__connectionVisual, []))
        ]
    
    def __str__(self):
        return _("Connection between %s and %s is shown on diagram %s") % (
            self.__connectionObject.GetSource().GetName(),
            self.__connectionObject.GetDestination().GetName(),
            self.__diagram.GetName()
        ) 

    def GetConnectionVisual(self):
        return self.__connectionVisual
