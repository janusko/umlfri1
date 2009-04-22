# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation
from lib.Drawing import  CElement




class CAddElementCmd(CHistoryOperation):
    
    def __init__(self, diagram, elementObject, pos, description = None): 
        CHistoryOperation.__init__(self, description)
        self.Diagram = diagram
        self.ElementObject = elementObject
        self.pos = pos


    def do (self):
        self.newElement = CElement(self.Diagram, self.ElementObject)
        self.newElement.SetPosition(self.pos)
        if self.description == None:
            self.description = _('Add new %s element on %s, %s') %(self.newElement.GetObject().GetName(), str(self.pos[0]), str(self.pos[1]))


    def undo(self):
        self.newElement.Deselect()
        self.newElement.GetObject().RemoveAppears(self.Diagram)
        self.Diagram.DeleteElement(self.newElement)      
        
        
    def redo(self):
        self.Diagram.AddElement(self.newElement)
        self.newElement.GetObject().AddAppears(self.Diagram)
 