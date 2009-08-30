from lib.Commands import CBaseCommand
from lib.Drawing import  CElement


class CCutCmd(CBaseCommand):
    
    def __init__(self, diagram, clipboard, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.clipboard = clipboard
        self.old_content = self.clipboard.content
        self.content = []
        for el in self.diagram.selected:
            if isinstance(el, CElement):
                self.content.append(el)

    def do (self):
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
            #if self.description == None:
                #self.description = _('Cutting selection')
        else:
            self.enabled = False

    def undo(self):
        for element in self.content:
            self.diagram.AddElement(element)
            element.GetObject().AddAppears(self.diagram)
        for con in self.delCon:
            if con not in self.diagram.connections: 
                self.diagram.AddConnection(con)            
        self.clipboard.content = self.old_content       

    def getDescription(self):
        if self.description != None:
            return self.description
        else:
            return _('Cutting selection')
        