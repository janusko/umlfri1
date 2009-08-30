from lib.Commands import CBaseCommand


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
            #if self.description == None:
                #if self.old_value == '':
                    #self.description = _('Setting diagram name to "%s"') %(self.value)
                #elif self.value == '':
                    #self.description = _('Clearing the old "%s" diagram name') %(self.old_value)                
                #else:
                    #self.description = _('Changing diagram name from "%s" to "%s"') %(self.old_value, self.value)
           
    def undo(self):

        self.diagram.SetName(self.old_value)
        
    def redo(self):
        self.diagram.SetName(self.value)
        
    def getDescription(self):
        if self.description != None:
            return self.description
        else:
            if self.old_value == '':
                return _('Setting diagram name to "%s"') %(self.value)
            elif self.value == '':
                return _('Clearing the old "%s" diagram name') %(self.old_value)                
            else:
                return _('Changing diagram name from "%s" to "%s"') %(self.old_value, self.value)

