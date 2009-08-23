from lib.Commands import CBaseCommand


class CDeleteTwElementCmd(CBaseCommand):
    
    def __init__(self, project,  node, description = None): 
        CBaseCommand.__init__(self, description)
        self.node = node
        self.project = project
        self.parent = self.node.GetParent()
        

    def removeFromArea(self, node):

        for j in node.GetChilds():
            self.removeFromArea(j)
            
        for con in node.GetObject().GetConnections():
            source = con.GetSource()
            destination = con.GetDestination()
            self.deletedConnections.append((con,source,destination))            
            source.RemoveConnection(con)
            destination.RemoveConnection(con)              
    
        for diagram in node.GetAppears():
            for element in diagram.GetElements():
                if element.GetObject() is node.GetObject():
                    self.deletedDiagramElements.append((element,diagram))
                    for con in diagram.GetConnections():
                        if (con.GetSource() is element) or (con.GetDestination() is element):
                            self.deletedDiagramConnections.append((con,diagram)) 
                    diagram.DeleteObject(element.GetObject())            


    def do (self):
        self.deletedDiagramElements = []
        self.deletedDiagramConnections = []
        self.deletedConnections = []

        self.removeFromArea(self.node)
        self.project.RemoveNode(self.node)            
            
        if self.description == None:
            self.description = _('Removing %s from project') %(self.node.GetObject().GetName())

        
    def undo(self):

        self.project.AddNode(self.node, self.parent)
        for element, diagram in self.deletedDiagramElements:
            diagram.AddElement(element)
        
        for con,s,d in self.deletedConnections:
            s.AddConnection(con)
            d.AddConnection(con)      
            
        for con, d in self.deletedDiagramConnections:
            if con not in d.connections: 
                d.AddConnection(con)       

