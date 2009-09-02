from lib.Commands import CBaseCommand


class CAddTwElementCmd(CBaseCommand):
    
    def __init__(self, project, node, parent): 
        CBaseCommand.__init__(self)
        self.project = project
        self.node = node
        self.parent = parent
        
    def Do (self):
        self.project.AddNode(self.node, self.parent)
        
    def Undo(self):
        self.project.RemoveNode(self.node)

    def GetDescription(self):
        return _('Adding %s to project') %(self.node.GetObject().GetName())
