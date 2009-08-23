from lib.Commands import CBaseCommand
from lib.Drawing import  CElement


class CElementAppendItemCmd(CBaseCommand):
    
    def __init__(self, element, key, description = None): 
        CBaseCommand.__init__(self, description)
        self.element = element
        self.key = key
       

    def do (self):
        
        self.element.GetObject().AppendItem(self.key)
        self.attList = self.element.GetObject().GetValue(self.key)
        self.appendedItem = self.attList[-1:][0]
        
        if self.description == None:
            if isinstance(self.element, CElement):
                name = self.element.GetObject().GetName()
            else:
                name = self.element.GetObject().GetType().GetId()
            self.description = _('Adding item to %s %s') %(name, self.key)
           
           
    def undo(self):
        self.attList.remove(self.appendedItem)
            
    def redo(self):
        self.attList.append(self.appendedItem)
 











