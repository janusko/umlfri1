# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import  CElement
from lib.Drawing import CDiagram



class CDiagramChangeCmd(CBaseCommand):
    
    def __init__(self, diagram, value, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.value = value

    def do (self):
        self.old_value = self.diagram.GetName()
        if self.old_value == self.value:
            self.enabled = False
        else:        
            self.diagram.SetName(self.value)
            if self.description == None:
                self.description = _('Changing diagram name from %s to %s') %(self.old_value, self.value)
           
    def undo(self):

        self.diagram.SetName(self.old_value)
        
    def redo(self):
        self.diagram.SetName(self.value)
 