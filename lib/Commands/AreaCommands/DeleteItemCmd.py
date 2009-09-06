from lib.Commands import CBaseCommand
from lib.Drawing import CElement, CConnection, CConLabelInfo


class CDeleteItemCmd(CBaseCommand):

    def __init__(self, diagram, item): 
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.item = item

    def Do(self):
        self.item.Deselect()
        self.delCon = []
        if isinstance(self.item , CElement):
            for con in self.diagram.GetConnections():
                if (con.GetSource() is self.item) or (con.GetDestination() is self.item):
                    self.delCon.append(con) 
            self.item.GetObject().RemoveAppears(self.diagram)
            if self.diagram.HasElement(self.item):
                self.diagram.DeleteItem(self.item)
        elif isinstance(self.item , CConnection):
            if self.diagram.HasConnectionBool(self.item):            
                self.diagram.DeleteItem(self.item)
        elif isinstance(self.item , CConLabelInfo):
            if self.diagram.HasConnectionBool(self.item.GetConnection()):
                con = self.item.GetConnection()
                self.diagram.DeleteItem(self.item.GetConnection())
                self.item.Deselect()
                self.item = con

    def Undo(self):
        if isinstance(self.item , CElement):
            self.item.object.AddAppears(self.diagram)
            self.diagram.AddElement(self.item )
            for con in self.delCon:
                if con not in self.diagram.connections: 
                    self.diagram.AddConnection(con)

        elif isinstance(self.item , CConnection):
            if not self.diagram.HasConnectionBool(self.item):
                self.diagram.AddConnection(self.item)

    def GetDescription(self):
        if isinstance(self.item , CElement):
            return _('Deleting %s from %s') %(self.item.GetObject().GetName(), self.diagram.GetName())
        elif isinstance(self.item , CConnection):
            return _('Deleting %s connection from "%s" diagram') %(self.item.GetObject().GetType().GetId(), self.diagram.GetName())
           