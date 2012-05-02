from lib.Commands import CBaseCommand


class CAddDiagramCmd(CBaseCommand):
    
    def __init__(self, diagram, node): 
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.node = node
        
    def Do(self):
        self.diagram.SetPath(self.node.GetPath() + "/" + self.diagram.GetName() + ":=Diagram=")
        self.node.AddDiagram(self.diagram)
       
    def Undo(self):
        self.node.RemoveDiagram(self.diagram)

    def GetDescription(self):
        return _('Adding %s to project') %(self.diagram.GetName())
