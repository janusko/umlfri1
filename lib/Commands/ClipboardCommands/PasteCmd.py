# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Drawing import  CElement
from lib.Exceptions.UMLException import UMLException

from lib.Exceptions.UserException import DrawingError
from lib.Project import CProject, CProjectNode


class CPasteCmd(CBaseCommand):
    
    def __init__(self, diagram, clipboard, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.clipboard = clipboard
        #self.old_content = self.clipboard.content
        
    def do (self):
        if self.clipboard.content:
            self.pasted = []
            for element in self.clipboard.content:
                try:
                    el = CElement(self.diagram, element.GetObject())
                except UMLException, e:
                    # to do: rewrite exception messages IN TRUNK, so they make sense to user when
                    # used in user exceptions... get rid of the programmer stuff...
                    cause = str(e)
                    if 'DiagramHaveNotThisElement' in cause:
                        text = 'This diagram can not have this element.'
                    elif 'ElementAlreadyExists' in cause:
                        text = 'This element already exists on this diagram'
                    else:
                        text = cause
                    
                    for el in self.pasted:
                        self.diagram.DeleteElement(el)
                    raise DrawingError(text)
                
                self.diagram.AddToSelection(el)
                el.CopyFromElement(element)
                self.pasted.append(el)


            if self.description == None:
                self.description = _('Pasting selection')
        else:
            self.enabled = False

    def undo(self):
        #self.clipboard.content = self.old_content 
        for el in self.pasted:
            el.Deselect()
            el.GetObject().RemoveAppears(self.diagram)
            self.diagram.DeleteElement(el)
            

    def redo(self):
        #self.clipboard.content = self.pasted
        for el in self.pasted:
            el.GetObject().AddAppears(self.diagram)
            self.diagram.AddElement(el)
        
        
        
        