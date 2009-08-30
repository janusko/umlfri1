from lib.Commands import CBaseCommand
from lib.Drawing import  CElement

class CCopyCmd(CBaseCommand):
    
    def __init__(self, diagram, clipboard, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.clipboard = clipboard
        self.content = []
        

    def do (self):
        
        for el in self.diagram.selected:
            if isinstance(el, CElement):
                self.content.append(el)
        
        if self.content:            
            self.old_content = self.clipboard.content
            self.clipboard.content = self.content
           
            #if self.description == None:
                #self.description = _('Copying selection')
        else:
            self.enabled = False

    def undo(self):
        self.clipboard.content = self.old_content
   
    def redo(self):
        self.clipboard.content = self.content
        
    def getDescription(self):
        if self.description != None:
            return self.description
        else:
            return _('Copying selection')
            