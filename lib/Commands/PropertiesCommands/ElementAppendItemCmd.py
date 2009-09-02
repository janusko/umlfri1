from lib.Commands import CBaseCommand
from lib.Drawing import  CElement


class CElementAppendItemCmd(CBaseCommand):
    
    def __init__(self, element, key): 
        CBaseCommand.__init__(self)
        self.element = element
        self.key = key

    def Do (self):
        self.element.GetObject().AppendItem(self.key)
        self.attList = self.element.GetObject().GetValue(self.key)
        self.appendedItem = self.attList[-1:][0]
           
    def Undo(self):
        self.attList.remove(self.appendedItem)
            
    def Redo(self):
        self.attList.append(self.appendedItem)

    def GetDescription(self):
        if isinstance(self.element, CElement):
            name = self.element.GetObject().GetName()
        else:
            name = self.element.GetObject().GetType().GetId()
        return _('Adding item to %s %s') %(name, self.key)
