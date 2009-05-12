# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import  CElement
from lib.Drawing import CDiagram


class CElementAppendItemCmd(CBaseCommand):
    
    def __init__(self, element, key, description = None): 
        CBaseCommand.__init__(self, description)
        self.element = element
        self.key = key
       

    def do (self):
        
        self.element.GetObject().AppendItem(self.key)
        
        if self.description == None:
            if isinstance(self.element, CElement):
                name = self.element.GetObject().GetName()
            else:
                name = self.element.GetObject().GetType().GetId()
            self.description = _('Adding item to %s %s') %(name, self.key)
           
           
    def undo(self):
        value = self.element.GetObject().GetValue(self.key) 
        value.pop(len(value)-1)


    def redo(self):
        self.element.GetObject().AppendItem(self.key)
 











