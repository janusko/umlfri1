# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation
from lib.Connections import CConnectionObject
from lib.Drawing import CConnection


class CPurgeConnectionCmd(CHistoryOperation):
    def __init__(self, connection, description = None): 
        CHistoryOperation.__init__(self, description)
        self.connection = connection
        self.diagram = self.connection.diagram 
        

    def do (self):
        
        self.source = self.connection.GetObject().GetSource()
        self.destination = self.connection.GetObject().GetDestination()
        #for appear in self.connection.GetObject().GetAppears():
        self.diagram.ShiftDeleteConnection(self.connection)  
               
        if self.description == None:
            self.description = _('Purging (deleting) %s connection from project') %(self.connection.GetObject().GetType().GetId())


    def redo(self):
        self.connection.Deselect()
        self.diagram.ShiftDeleteConnection(self.connection)      
        
        
    def undo(self):
        
        self.destination.AddConnection(self.connection.GetObject()) 
        self.source.AddConnection(self.connection.GetObject()) 
        for appear in self.connection.GetObject().GetAppears():
            if self.connection not in appear.connections:
                appear.AddConnection(self.connection)
            
