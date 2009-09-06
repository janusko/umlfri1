from lib.Commands import CBaseCommand
from lib.Drawing import  CElement


class CDragAndDropElementCmd(CBaseCommand):
    
    def __init__(self, newElement, pos): 
        CBaseCommand.__init__(self)
        self.diagram = newElement.GetDiagram()
        self.element = newElement
        self.pos = pos

    def Do(self):
        self.element.SetPosition(self.pos)
        
    def Undo(self):
        self.delCon = []
        for con in self.diagram.GetConnections():
            if (con.GetSource() is self.element) or (con.GetDestination() is self.element):
                self.delCon.append(con)         
        self.element.Deselect()
        self.element.GetObject().RemoveAppears(self.diagram)
        self.diagram.DeleteElement(self.element)        
        
    def Redo(self):
        self.Do()
        self.diagram.AddElement(self.element)
        self.element.GetObject().AddAppears(self.diagram)
        if self.delCon:
            for con in self.delCon:
                if con not in self.diagram.connections: 
                    self.diagram.AddConnection(con)

    def GetDescription(self):
        return _('Drag\'n\'drop %s to %s from treeview') %(self.element.GetObject().GetName(), self.diagram.GetName())
