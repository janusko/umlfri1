# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation
from lib.Drawing import CElement, CConnection


class CMoveSelectionCmd(CHistoryOperation):
    
    def __init__(self, diagram, canvas, delta, description = None):
        CHistoryOperation.__init__(self, description)
        self.diagram = diagram
        self.canvas = canvas
        self.delta = delta
        self.oldDelta = None


    def do (self):
        self.oldDelta = self.delta
        self.selection = self.diagram.selected
        self.diagram.MoveSelection(self.delta, self.canvas)
                
        if self.description == None:
            if len(self.selection) == 1:
                for el in self.diagram.GetSelectedElements():
                    if isinstance(el , CElement):
                        self.description = _('Moving %s on %s') %(el.GetObject().GetName(), self.diagram.GetName())
                    else:
                        self.description = _('Moving %s label on %s') %(el.GetObject().GetType().GetId(), self.diagram.GetName())
                
            else:
                self.description = _('Moving selection of:')
                for el in self.diagram.GetSelectedElements():
                    self.description += '\n\t%s' %(el.GetObject().GetName())
                

    def undo(self):
        oldSelection = self.diagram.GetSelected()
        self.diagram.DeselectAll()
        self.diagram.selected = tuple(self.selection)
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







