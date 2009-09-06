from lib.Commands import CBaseCommand
from lib.Project import CProjectNode

class CCreateElementCmd(CBaseCommand):

    def __init__(self, project, diagram, element_object, parent_element = None): 
        CBaseCommand.__init__(self)
        self.project = project
        self.diagram = diagram
        if parent_element is None:
            path = diagram.GetPath()
        else:
            path = parent_element.GetPath()

        self.parent = self.project.GetNode(path)
        self.node = CProjectNode(self.parent, element_object, self.parent.GetPath() + "/" + element_object.GetName() + ":" + element_object.GetType().GetId())

    def Do(self):
        self.project.AddNode(self.node, self.parent)
        
    def Undo(self):
        self.project.RemoveNode(self.node)

    def GetDescription(self):
        return _('Adding %s to project') %(self.node.GetObject().GetName())
