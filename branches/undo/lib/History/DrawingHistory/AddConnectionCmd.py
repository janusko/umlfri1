# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation
from lib.Connections import CConnectionObject
from lib.Drawing import CConnection


class CAddConnectionCmd(CHistoryOperation):
    def __init__(self, diagram, connectionData, destination, description = None): 
        CHistoryOperation.__init__(self, description)
        self.diagram = diagram
        self.connectionData = connectionData
        self.destination = destination
        

    def do (self):
        (type, points, source) = self.connectionData 
        self.connectionObject = CConnectionObject(type, source.GetObject(), self.destination.GetObject())
        self.connection = CConnection(self.diagram, self.connectionObject, source, self.destination, points[1:])
        
        if self.description == None:
            self.description = _('Adding %s connection to %s') %(self.connection.GetObject().GetType().GetId(), self.diagram.GetName())


    def undo(self):
        self.connection.Deselect()
        self.diagram.ShiftDeleteConnection(self.connection)      
        
        
    def redo(self):
        source = self.connectionData[2] 
        self.destination.GetObject().AddConnection(self.connection.GetObject()) 
        source.GetObject().AddConnection(self.connection.GetObject()) 
       
        if self.connection not in self.diagram.connections:
            self.diagram.AddConnection(self.connection)
            

            
    