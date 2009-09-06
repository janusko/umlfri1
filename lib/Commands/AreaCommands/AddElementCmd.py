from lib.Commands.ProjectViewCommands import CCreateElementCmd
from lib.Drawing import  CElement
from lib.Elements import CElementObject


class CAddElementCmd(CCreateElementCmd):
    
    def __init__(self, project, diagram, canvas, selected_type, position):
        self.canvas = canvas
        self.pos = position
        self.element = CElement(diagram, CElementObject(project.GetMetamodel().GetElementFactory().GetElement(selected_type)))
        self.delCon = []
        parentElement = None
        
        # need to do this only once in __init__
        # I get parent element of selected elements (if element is on (over) another element)
        minzorder = 9999999
        for el in diagram.GetSelectedElements():
            pos1, pos2 = el.GetSquare(self.canvas)
            zorder = diagram.elements.index(el)
            if self.element.AreYouInRange(self.canvas, pos1, pos2, True):
                for el2 in diagram.GetElementsInRange(self.canvas, pos1, pos2, True):
                    if diagram.elements.index(el2) < minzorder:        # get element with minimal zorder
                        minzorder = diagram.elements.index(el2)
                        parentElement = el2.GetObject()
        CCreateElementCmd.__init__(self, project, diagram, self.element.GetObject(), parentElement)

    def Do(self):
        self.element.SetPosition(self.pos)
        CCreateElementCmd.Do(self)

    def Undo(self):
        self.delCon = []
        for con in self.diagram.GetConnections():
            if (con.GetSource() is self.element) or (con.GetDestination() is self.element):
                self.delCon.append(con)         
        self.element.Deselect()
        self.element.GetObject().RemoveAppears(self.diagram)
        self.diagram.DeleteElement(self.element)        
        CCreateElementCmd.Undo(self)

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
