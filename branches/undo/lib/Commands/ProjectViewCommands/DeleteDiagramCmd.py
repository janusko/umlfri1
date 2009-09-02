from lib.Commands import CBaseCommand


class CDeleteDiagramCmd(CBaseCommand):
    
    def __init__(self, diagram, node): 
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.node = node
        
    def Do (self):
        self.node.RemoveDiagram(self.diagram)

    def Undo(self):
        self.node.AddDiagram(self.diagram)

    def GetDescription(self):
        return _('Deleting %s diagram from project') %(self.diagram.GetName())
