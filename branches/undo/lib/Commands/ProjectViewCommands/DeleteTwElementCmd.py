from lib.Commands import CBaseCommand


class CDeleteTwElementCmd(CBaseCommand):
    
    def __init__(self, project,  node): 
        CBaseCommand.__init__(self)
        self.node = node
        self.project = project

    def _RemoveFromArea(self, node):
        for j in node.GetChilds():
            self._RemoveFromArea(j)
            
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


    def Do(self):
        self.parent = self.node.GetParent()
        self.deletedDiagramElements = []
        self.deletedDiagramConnections = []
        self.deletedConnections = []
        self._RemoveFromArea(self.node)
        self.project.RemoveNode(self.node)            
                
    def Undo(self):
        self.project.AddNode(self.node, self.parent)
        for element, diagram in self.deletedDiagramElements:
            diagram.AddElement(element)
        
        for con,s,d in self.deletedConnections:
            s.AddConnection(con)
            d.AddConnection(con)      
            
        for con, d in self.deletedDiagramConnections:
            if con not in d.connections: 
                d.AddConnection(con)       

    def GetDescription(self):
        return _('Removing %s from project') %(self.node.GetObject().GetName())
