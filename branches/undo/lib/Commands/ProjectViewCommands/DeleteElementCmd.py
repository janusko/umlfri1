from lib.Commands import CBaseCommand


class CDeleteElementCmd(CBaseCommand):

    def __init__(self, project,  node): 
        CBaseCommand.__init__(self)
        self.element_object = node.object
        self.project = project  
        self.deletedConnections = []
        self.node = node 
        self.parent = self.node.GetParent()

        self.myAppears = []
        for i in self.element_object.appears:
            self.myAppears.append(i)

    def Do (self):
        self.ctd = []
        for con in self.element_object.GetConnections():
            source = con.GetSource()
            destination = con.GetDestination()
            self.ctd.append((con,source,destination))
            
        for con,s,d in self.ctd:
            s.RemoveConnection(con)
            d.RemoveConnection(con)   
        
        self.removedAppears = []
        for diagram in self.myAppears:
            if diagram().HasElementObject(self.element_object): 
                appearedConnections = []
                for con in diagram().GetConnections():
                    if (con.GetSource().GetObject() is self.element_object) or (con.GetDestination().GetObject() is self.element_object):
                        appearedConnections.append(con)
        
                self.deletedConnections.append(appearedConnections)
                self.removedAppears.append([diagram, diagram().HasElementObject(self.element_object)])
                
            diagram().DeleteObject(self.element_object)
        self.project.RemoveNode(self.node)            
       
    def Undo(self):
        for con,s,d in self.ctd:
            s.AddConnection(con)
            d.AddConnection(con)        
        self.project.AddNode(self.node, self.parent)
        i = 0
        for diagram, el in self.removedAppears:
            if diagram().HasElementObject(el) == None:
                diagram().AddElement(el)
                for con in self.deletedConnections[i]:
                    diagram().AddConnection(con)
            i =+ 1

    def GetDescription(self):
        return _('Deleting "%s" from project') %(self.element_object.GetName())
