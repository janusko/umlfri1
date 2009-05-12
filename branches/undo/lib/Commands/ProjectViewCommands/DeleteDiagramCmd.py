# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand


class CDeleteDiagramCmd(CBaseCommand):
    
    def __init__(self, diagram, node, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.node = node
        
    def do (self):
        self.node.RemoveDiagram(self.diagram)

        if self.description == None:
            self.description = _('Deleting %s diagram from project') %(self.diagram.GetName())


    def undo(self):
        self.node.AddDiagram(self.diagram)

    def redo(self):
        self.do()
     