from lib.Commands import CBaseCommand
from lib.Connections import CConnectionObject
from lib.Drawing import CConnection


class CPurgeConnectionCmd(CBaseCommand):
    def __init__(self, connection, description = None): 
        CBaseCommand.__init__(self, description)
        self.connection = connection
        self.diagram = self.connection.diagram() 
        self.source = self.connection.GetObject().GetSource()
        self.destination = self.connection.GetObject().GetDestination()

    def do (self):
        self.connection.Deselect()
        
        for appear in self.connection.GetObject().GetAppears():
            appear.DeleteConnectionObject(self.connection.GetObject())
        
        if self.connection.GetObject() in self.source.connections:
            self.source.RemoveConnection(self.connection.GetObject())
        if self.connection.GetObject() in self.destination.connections:
            self.destination.RemoveConnection(self.connection.GetObject())
           
        if self.description == None:
            self.description = _('Deleting %s connection from project') %(self.connection.GetObject().GetType().GetId())

        
    def undo(self):
        
        self.destination.AddConnection(self.connection.GetObject()) 
        self.source.AddConnection(self.connection.GetObject()) 
        if self.connection not in self.diagram.connections:
            self.diagram.AddConnection(self.connection)
           
