# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import  CElement 


class CElementDeleteItemCmd(CBaseCommand):
    
    def __init__(self, element, key, description = None): 
        CBaseCommand.__init__(self, description)
        self.element = element
        self.key = key
        self.myKey = self.key.rsplit('[',1)[0]
        self.attList = self.element.GetObject().GetValue(self.myKey)        

    def do (self):
        
        if len(self.attList) <= 1: # this will never happen... shouldn't at least :)
            self.enabled = False
      
        else:
            self.itemToDelete = self.element.GetObject().GetValue(self.key) 
            self.myIndex = self.attList.index(self.itemToDelete)
            self.attList.remove(self.itemToDelete)
                       
            if self.description == None:
                if isinstance(self.element, CElement):
                    name = self.element.GetObject().GetName()
                else:
                    name = self.element.GetObject().GetType().GetId()
                
                if '.' in self.myKey:
                    itemName = self.myKey.rsplit('.',1)[1][:-1]
                else:
                    itemName = self.myKey[:-1]
                self.description = _('Deleting %i. %s from %s') %(self.myIndex, itemName, name)
                
           
    def undo(self):
        self.attList.insert(self.myIndex, self.itemToDelete)


    def redo(self):
        self.attList.remove(self.itemToDelete)

