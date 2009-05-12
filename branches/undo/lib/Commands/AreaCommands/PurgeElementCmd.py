# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import  CElement

from lib.Project import CProject, CProjectNode


class CPurgeElementCmd(CBaseCommand):
    
    def __init__(self, newElement, application, description = None): 
        CBaseCommand.__init__(self, description)
        self.element = newElement
        self.application = application  
        self.deletedConnections = []
        self.node = self.application.GetProject().Find(self.element.GetObject().GetName())
        self.parent = self.node.GetParent()

        self.myAppears = []
        for i in self.element.GetObject().appears:
            self.myAppears.append(i)
        self.element.Deselect()
        

    def do (self):
        self.ctd = []
        for con in self.element.GetObject().GetConnections():
            #self.element.GetObject().RemoveConnection(con)
            source = con.GetSource()
            destination = con.GetDestination()
            self.ctd.append((con,source,destination))
            
        for con,s,d in self.ctd:
            s.RemoveConnection(con)
            d.RemoveConnection(con)   
        
        self.removedAppears = []
        for diagram in self.myAppears:
            if self.element in diagram.elements:
                appearedConnections = []
                for con in diagram.GetConnections():
                    if (con.GetSource() is self.element) or (con.GetDestination() is self.element):
                        appearedConnections.append(con)
        
                self.deletedConnections.append(appearedConnections)
                self.removedAppears.append(diagram)
                
            diagram.DeleteObject(self.element.GetObject())
        self.application.GetProject().RemoveNode(self.node)            
        
        if self.description == None:
            self.description = _('Deleting %s from project') %(self.element.GetObject().GetName())

    def undo(self):
        for con,s,d in self.ctd:
            s.AddConnection(con)
            d.AddConnection(con)        
        self.application.GetProject().AddNode(self.node, self.parent)
        i = 0
        for diagram in self.removedAppears:
            if self.element not in diagram.elements:
                diagram.AddElement(self.element)
                for con in self.deletedConnections[i]:
                    diagram.AddConnection(con)
            i =+ 1
       
   