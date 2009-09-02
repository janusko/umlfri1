from lib.Commands import CBaseCommand
from lib.Drawing import CElement, CConnection


class CMoveSelectionCmd(CBaseCommand):
    
    def __init__(self, diagram, canvas, delta):
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.canvas = canvas
        self.delta = delta

    def Do (self):
        self.selection = []
        for s in self.diagram.GetSelected():
            self.selection.append(s)
        self.selection = set(self.selection)    
        self.diagram.MoveSelection(self.delta, self.canvas)

    def Undo(self):
        oldSelection = self.diagram.GetSelected()
        self.diagram.DeselectAll()
        for s in self.selection:
            self.diagram.AddToSelection(s)        
        self.diagram.MoveSelection((-self.delta[0], -self.delta[1]), self.canvas)
        self.diagram.DeselectAll()
        for s in oldSelection:
            self.diagram.AddToSelection(s)
        
    def Redo(self):
        oldSelection = self.diagram.GetSelectedElements()
        self.diagram.DeselectAll()
        for s in self.selection:
            self.diagram.AddToSelection(s)
        self.diagram.MoveSelection(self.delta, self.canvas)
        self.diagram.DeselectAll()
        for s in oldSelection:
            self.diagram.AddToSelection(s)

    def GetDescription(self):
        if len(self.selection) == 1:
            for el in self.selection:
                if isinstance(el , CElement):
                    return _('Moving %s on %s') %(el.GetObject().GetName(), self.diagram.GetName())
                else:
                    return _('Moving %s label on %s') %(el.GetObject().GetType().GetId(), self.diagram.GetName())
        else:
            return _('Moving selection on %s') %(self.diagram.GetName())            
