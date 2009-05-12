# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import  CElement

from lib.Project import CProject, CProjectNode


class CAddElementCmd(CBaseCommand):
    
    def __init__(self, newElement, pos, parentElement = None, application = None, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = newElement.diagram
        self.element = newElement
        self.parentElement = parentElement
        self.pos = pos
        self.application = application 

    def do (self):
        
        self.element.SetPosition(self.pos)
        if self.application is not None:
            if self.parentElement is None:
                path = self.diagram.GetPath()
            else:
                path = parentElement.GetPath()
                
            self.parent = self.application.GetProject().GetNode(path)
            self.node = CProjectNode(self.parent, self.element.GetObject(), self.parent.GetPath() + "/" + self.element.GetObject().GetName() + ":" + self.element.GetObject().GetType().GetId())
            self.application.GetProject().AddNode(self.node, self.parent)
            
        if self.description == None:
            self.description = _('Adding %s to %s') %(self.element.GetObject().GetName(), self.diagram.GetName())


    def undo(self):
        self.element.Deselect()
        self.element.GetObject().RemoveAppears(self.diagram)
        self.diagram.DeleteElement(self.element)        
        
        if self.application is not None:
            self.application.GetProject().RemoveNode(self.node)
        
        
    def redo(self):
        self.do()
        self.diagram.AddElement(self.element)
        self.element.GetObject().AddAppears(self.diagram)
       
 