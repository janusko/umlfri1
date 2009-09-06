from lib.Commands import CBaseCommand
from lib.Drawing import  CElement


class CCutCmd(CBaseCommand):
    
    def __init__(self, diagram, clipboard): 
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.clipboard = clipboard
        self.content = []
        
    def Do(self):
        self.old_content = self.clipboard.content
        
        for el in self.diagram.selected:
            if isinstance(el, CElement):
                self.content.append(el)       

        self.delCon = []        
        if self.content:
            self.diagram.DeselectAll()
            self.clipboard.content = self.content
            for el in self.content:
                el.Deselect()
                for con in self.diagram.GetConnections():
                    if (con.GetSource() is el) or (con.GetDestination() is el) and (con not in self.delCon):
                        self.delCon.append(con)                 
                self.diagram.DeleteElement(el)
                el.GetObject().RemoveAppears(self.diagram)
        else:
            self._SetEnabled(False)

    def Undo(self):
        for element in self.content:
            self.diagram.AddElement(element)
            element.GetObject().AddAppears(self.diagram)
        for con in self.delCon:
            if con not in self.diagram.connections: 
                self.diagram.AddConnection(con)            
        self.clipboard.content = self.old_content       

    def GetDescription(self):
        return _('Cutting selection')
