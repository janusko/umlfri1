# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import  CElement



class CCutCmd(CBaseCommand):
    
    def __init__(self, diagram, clipboard, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.clipboard = clipboard
        self.old_content = self.clipboard.content
        self.content = []
        for el in self.diagram.selected:
            if isinstance(el, CElement):
                self.content.append(el)


    def do (self):
        if self.content:
            self.diagram.DeselectAll()
            self.clipboard.content = self.content
            for el in self.content:
                el.Deselect()
                self.diagram.DeleteElement(el)
                el.GetObject().RemoveAppears(self.diagram)
            
            if self.description == None:
                self.description = _('Cutting selection')
        else:
            self.enabled = False


    def undo(self):
        for element in self.content:
            self.diagram.AddElement(element)
            element.GetObject().AddAppears(self.diagram)
        self.clipboard.content = self.old_content       


    def redo(self):
        self.do()
        
        