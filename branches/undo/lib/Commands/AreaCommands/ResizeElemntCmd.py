# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand


class CResizeElemntCmd(CBaseCommand):
    def __init__(self, element, canvas, delta, selSq, description = None): 
        CBaseCommand.__init__(self, description)
        self.element = element
        self.canvas = canvas
        self.delta = delta
        self.selSq = selSq


    def do (self):
        self.element.Resize(self.canvas, self.delta, self.selSq)
        if self.description == None:
            self.description = _('Resizing %s on %s') %(self.element.GetObject().GetName(), self.element.diagram.GetName())


    def undo(self):
        self.element.Resize(self.canvas, (-self.delta[0], -self.delta[1]), self.selSq)


    def redo(self):
        self.element.Resize(self.canvas, self.delta, self.selSq)
        
        