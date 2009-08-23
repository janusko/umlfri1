from lib.Commands import CBaseCommand


class CAddTwElementCmd(CBaseCommand):
    
    def __init__(self, project, node, parent, description = None): 
        CBaseCommand.__init__(self, description)
        self.project = project
        self.node = node
        self.parent = parent
        
    def do (self):
        self.project.AddNode(self.node, self.parent)
        if self.description == None:
            self.description = _('Adding %s to project') %(self.node.GetObject().GetName())

    def undo(self):
        self.project.RemoveNode(self.node)

     