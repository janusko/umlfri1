from lib.Commands import CBaseCommand
from lib.Connections import CConnectionObject
from lib.Drawing import CConnection


class CAddConnectionCmd(CBaseCommand):
    def __init__(self, diagram, connectionObject, source, destination, points= None):     
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.connectionObject = connectionObject
        self.source = source
        self.destination = destination
        self.points = points
        
    def Do(self):
        self.connection = CConnection(self.diagram, self.connectionObject, self.source, self.destination, self.points)

    def Undo(self):
        self.connection.Deselect()
        self.diagram.ShiftDeleteConnection(self.connection)      

    def Redo(self):
        self.destination.GetObject().AddConnection(self.connection.GetObject()) 
        self.source.GetObject().AddConnection(self.connection.GetObject()) 
        
        if self.connection not in self.diagram.connections: 
            self.diagram.AddConnection(self.connection)
 
    def GetDescription(self):
        return _('Adding %s connection to %s') %(self.connection.GetObject().GetType().GetId(), self.diagram.GetName())
