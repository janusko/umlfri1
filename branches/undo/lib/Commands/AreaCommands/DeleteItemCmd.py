from lib.Commands import CBaseCommand
from lib.Drawing import CElement, CConnection


class CDeleteItemCmd(CBaseCommand):


    def __init__(self, diagram, item, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.item = item

    def do (self):
        self.item.Deselect()
        self.delCon = []
        if isinstance(self.item , CElement):
                       
            for con in self.diagram.GetConnections():
                if (con.GetSource() is self.item) or (con.GetDestination() is self.item):
                    self.delCon.append(con) 
            self.item.GetObject().RemoveAppears(self.diagram)
            if self.item in self.diagram.elements: 
                self.diagram.DeleteItem(self.item)
            
            #if self.description == None:
                #self.description = _('Deleting %s from %s') %(self.item.GetObject().GetName(), self.diagram.GetName())
            
        elif isinstance(self.item , CConnection):
            if self.item in self.diagram.connections: 
                self.diagram.DeleteItem(self.item)
                
            #if self.description == None:
                #self.description = _('Deleting %s connection from "%s" diagram') %(self.item.GetObject().GetType().GetId(), self.diagram.GetName())
    
    def undo(self):
        if isinstance(self.item , CElement):
            self.item.object.AddAppears(self.diagram)
            self.diagram.AddElement(self.item )

            for con in self.delCon:
                if con not in self.diagram.connections: 
                    self.diagram.AddConnection(con)

        elif isinstance(self.item , CConnection):
            if self.item not in self.diagram.connections: 
                self.diagram.AddConnection(self.item )

    def getDescription(self):
        if self.description != None:
            return self.description
        else:
            if isinstance(self.item , CElement):
                return _('Deleting %s from %s') %(self.item.GetObject().GetName(), self.diagram.GetName())
            elif isinstance(self.item , CConnection):
                return _('Deleting %s connection from "%s" diagram') %(self.item.GetObject().GetType().GetId(), self.diagram.GetName())
   
                
            
            
            