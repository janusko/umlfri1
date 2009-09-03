from lib.Commands import CBaseCommand


class CDiagramChangeCmd(CBaseCommand):
    
    def __init__(self, diagram, value): 
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.value = value

    def Do(self):
        self.old_value = self.diagram.GetName()
        if self.old_value == self.value:
            self.enabled = False
        else:        
            self.diagram.SetName(self.value)

    def Undo(self):
        self.diagram.SetName(self.old_value)
        
    def Redo(self):
        self.diagram.SetName(self.value)
        
    def GetDescription(self):
        if self.old_value == '':
            return _('Setting diagram name to "%s"') %(self.value)
        elif self.value == '':
            return _('Clearing the old "%s" diagram name') %(self.old_value)                
        else:
            return _('Changing diagram name from "%s" to "%s"') %(self.old_value, self.value)
