from lib.Commands import CBaseCommand
from lib.Drawing import  CElement
from lib.Project import CProject, CProjectNode



class CAddElementCmd(CBaseCommand):
    
    def __init__(self, newElement, pos, parentElement = None, project = None): 
        CBaseCommand.__init__(self)
        self.diagram = newElement.GetDiagram()
        self.element = newElement
        self.parentElement = parentElement
        self.pos = pos
        self.project = project 
        self.delCon = []

    def Do(self):
        self.element.SetPosition(self.pos)
        if self.project is not None:
            if self.parentElement is None:
                path = self.diagram.GetPath()
            else:
                path = parentElement.GetPath()
                
            self.parent = self.project.GetNode(path)
            self.node = CProjectNode(self.parent, self.element.GetObject(), self.parent.GetPath() + "/" + self.element.GetObject().GetName() + ":" + self.element.GetObject().GetType().GetId())
            self.project.AddNode(self.node, self.parent)

    def Undo(self):
        self.delCon = []
        for con in self.diagram.GetConnections():
            if (con.GetSource() is self.element) or (con.GetDestination() is self.element):
                self.delCon.append(con)         
        
        self.element.Deselect()
        self.element.GetObject().RemoveAppears(self.diagram)
        self.diagram.DeleteElement(self.element)        
        
        if self.project is not None:
            self.project.RemoveNode(self.node)
        else:
            pass

    def Redo(self):
        self.Do()
        self.diagram.AddElement(self.element)
        self.element.GetObject().AddAppears(self.diagram)
        if self.delCon:
            for con in self.delCon:
                if con not in self.diagram.connections: 
                    self.diagram.AddConnection(con)

    def GetDescription(self):
        return _('Adding %s to %s') %(self.element.GetObject().GetName(), self.diagram.GetName())
