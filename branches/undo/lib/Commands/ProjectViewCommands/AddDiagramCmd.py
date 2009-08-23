from lib.Commands import CBaseCommand


class CAddDiagramCmd(CBaseCommand):
    
    def __init__(self, diagram, node, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.node = node
        self.path = self.node.GetPath() + "/" + self.diagram.GetName() + ":=Diagram="
        
    def do (self):
        self.diagram.SetPath(self.path)
        self.node.AddDiagram(self.diagram)
        if self.description == None:
            self.description = _('Adding %s to project') %(self.diagram.GetName())

    def undo(self):
        self.node.RemoveDiagram(self.diagram)

     