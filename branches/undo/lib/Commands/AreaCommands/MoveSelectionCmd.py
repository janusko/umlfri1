# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import CElement, CConnection


class CMoveSelectionCmd(CBaseCommand):
    
    def __init__(self, diagram, canvas, delta, description = None):
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.canvas = canvas
        self.delta = delta


    def do (self):
        self.selection = []
        for s in self.diagram.GetSelected():
            self.selection.append(s)
        self.selection = set(self.selection)    
        self.diagram.MoveSelection(self.delta, self.canvas)
                
        if self.description == None:
            if len(self.selection) == 1:
                for el in self.diagram.GetSelectedElements():
                    if isinstance(el , CElement):
                        self.description = _('Moving %s on %s') %(el.GetObject().GetName(), self.diagram.GetName())
                    else:
                        self.description = _('Moving %s label on %s') %(el.GetObject().GetType().GetId(), self.diagram.GetName())
            else:
                self.description = _('Moving selection')
                

    def undo(self):
        oldSelection = self.diagram.GetSelected()
        self.diagram.DeselectAll()
        for s in self.selection:
            self.diagram.AddToSelection(s)        
        #self.diagram.selected = self.selection
        self.diagram.MoveSelection((-self.delta[0], -self.delta[1]), self.canvas)
        self.diagram.DeselectAll()
        for s in oldSelection:
            self.diagram.AddToSelection(s)
        
        
    def redo(self):
        oldSelection = self.diagram.GetSelectedElements()
        self.diagram.DeselectAll()
        for s in self.selection:
            self.diagram.AddToSelection(s)
        self.diagram.MoveSelection(self.delta, self.canvas)
        self.diagram.DeselectAll()
        for s in oldSelection:
            self.diagram.AddToSelection(s)


