# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand


class CAddTwElementCmd(CBaseCommand):
    
    def __init__(self, application, node, parent, description = None): 
        CBaseCommand.__init__(self, description)
        self.application = application
        self.node = node
        self.parent = parent
        
    def do (self):
        self.application.GetProject().AddNode(self.node, self.parent)
        if self.description == None:
            self.description = _('Adding %s to project') %(self.node.GetObject().GetName())

    def undo(self):
        self.application.GetProject().RemoveNode(self.node)

     