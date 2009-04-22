# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation
from lib.Drawing import CElement, CConnection





class CDeleteItemCmd(CHistoryOperation):


    def __init__(self, diagram, item, description = None): 
        CHistoryOperation.__init__(self, description)
        self.diagram = diagram
        self.item = item
        self.delCon = []


    def do (self):
        if isinstance(self.item , CElement):
            pos = self.item.GetPosition()
            self.item.Deselect()
            self.item.GetObject().RemoveAppears(self.diagram)
                        
            for con in self.diagram.GetConnections():
                if (con.GetSource() is self.item) or (con.GetDestination() is self.item):
                    self.delCon.append(con) 
            
            if self.description == None:
                self.description = _('Delete %s element from %s') %(self.item.GetObject().GetName(), self.diagram.GetName())
            
            
        elif isinstance(self.item , CConnection):
            if self.description == None:
                self.description = _('Delete %s connection from %s') %(self.item.GetObject().GetType().GetId(), self.diagram.GetName())
        
        self.diagram.DeleteItem(self.item )
        
    
    def undo(self):
        if isinstance(self.item , CElement):
            self.item.object.AddAppears(self.diagram)
            self.diagram.AddElement(self.item )
            
            for con in self.delCon:
                self.diagram.AddConnection(con)

        elif isinstance(self.item , CConnection):
            self.diagram.AddConnection(self.item )

                
    def redo(self):
       self.diagram.DeleteItem(self.item ) 
       if isinstance(self.item , CElement):
           self.item.GetObject().RemoveAppears(self.diagram)

