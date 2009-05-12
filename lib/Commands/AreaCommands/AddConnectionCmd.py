# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Connections import CConnectionObject
from lib.Drawing import CConnection


class CAddConnectionCmd(CBaseCommand):
    def __init__(self, diagram, connectionObject, source, destination, points= None, description = None):     
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.connectionObject = connectionObject
        self.source = source
        self.destination = destination
        self.points = points
        

    def do (self):
        self.connection = CConnection(self.diagram, self.connectionObject, self.source, self.destination, self.points)
        if self.description == None:
            self.description = _('Adding %s connection to %s') %(self.connection.GetObject().GetType().GetId(), self.diagram.GetName())


    def undo(self):
        self.connection.Deselect()
        self.diagram.ShiftDeleteConnection(self.connection)      
        
        
    def redo(self):
        self.destination.GetObject().AddConnection(self.connection.GetObject()) 
        self.source.GetObject().AddConnection(self.connection.GetObject()) 
       
        if self.connection not in self.diagram.connections:
            self.diagram.AddConnection(self.connection)
            
    