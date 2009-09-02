from lib.Commands import CBaseCommand
from lib.Drawing import  CElement


class CPurgeElementCmd(CBaseCommand):
    
    def __init__(self, newElement, project): 
        CBaseCommand.__init__(self)
        self.element = newElement
        self.project = project  
        self.deletedConnections = []
        self.node = self.element.GetObject().GetNode()
        self.parent = self.node.GetParent()

        self.myAppears = []
        for i in self.element.GetObject().appears:
            self.myAppears.append(i)
        self.element.Deselect()

    def Do (self):
        self.ctd = []
        for con in self.element.GetObject().GetConnections():
            source = con.GetSource()
            destination = con.GetDestination()
            self.ctd.append((con,source,destination))
            
        for con,s,d in self.ctd:
            s.RemoveConnection(con)
            d.RemoveConnection(con)   
        
        self.removedAppears = []
        for diagram in self.myAppears:
            if diagram().HasElement(self.element): 
                appearedConnections = []
                for con in diagram().GetConnections():
                    if (con.GetSource() is self.element) or (con.GetDestination() is self.element):
                        appearedConnections.append(con)
        
                self.deletedConnections.append(appearedConnections)
                self.removedAppears.append(diagram)
                
            diagram().DeleteObject(self.element.GetObject())
        self.project.RemoveNode(self.node)            

    def Undo(self):
        for con,s,d in self.ctd:
            s.AddConnection(con)
            d.AddConnection(con)        
        self.project.AddNode(self.node, self.parent)
        i = 0
        for diagram in self.removedAppears:
            if diagram().HasElement(self.element) == None:
                diagram().AddElement(self.element)
                for con in self.deletedConnections[i]:
                    diagram().AddConnection(con)
            i =+ 1

    def GetDescription(self):
        return _('Deleting "%s" from project') %(self.element.GetObject().GetName())
        