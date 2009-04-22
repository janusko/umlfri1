# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation
from lib.Drawing import  CElement




class CAddElementCmd(CHistoryOperation):
    
    def __init__(self, newElement, pos, description = None): 
        CHistoryOperation.__init__(self, description)
        self.diagram = newElement.diagram
        self.newElement = newElement
        #self.ElementObject = elementObject
        self.pos = pos


    def do (self):
        #self.newElement = CElement(self.diagram, self.ElementObject)
        self.newElement.SetPosition(self.pos)
        if self.description == None:
            self.description = _('Adding %s element to %s') %(self.newElement.GetObject().GetName(), self.diagram.GetName())


    def undo(self):
        self.newElement.Deselect()
        self.newElement.GetObject().RemoveAppears(self.diagram)
        self.diagram.DeleteElement(self.newElement)      
        
        
    def redo(self):
        self.diagram.AddElement(self.newElement)
        self.newElement.GetObject().AddAppears(self.diagram)
 