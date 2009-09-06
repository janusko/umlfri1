from lib.Commands import CBaseCommand
from lib.Drawing import  CElement

class CCopyCmd(CBaseCommand):
    
    def __init__(self, diagram, clipboard): 
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.clipboard = clipboard
        self.content = []

    def Do(self):
        for el in self.diagram.selected:
            if isinstance(el, CElement):
                self.content.append(el)
        
        if self.content:            
            self.old_content = self.clipboard.content
            self.clipboard.content = self.content
        else:
            self._SetEnabled(False)

    def Undo(self):
        self.clipboard.content = self.old_content
   
    def Redo(self):
        self.clipboard.content = self.content
        
    def GetDescription(self):
        return _('Copying selection')
