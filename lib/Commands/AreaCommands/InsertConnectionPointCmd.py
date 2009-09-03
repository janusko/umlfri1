from lib.Commands import CBaseCommand


class CInsertConnectionPointCmd(CBaseCommand):

    def __init__(self, connection, index, canvas, point): 
        CBaseCommand.__init__(self) 
        self.connection = connection
        self.index = index
        self.canvas = canvas
        self.point = point

    def Do(self):
        pos = max((0, self.point[0])), max((0, self.point[1]))
        prevPoint = self.connection.GetPoint(self.canvas, self.index)
        nextPoint = self.connection.GetPoint(self.canvas, self.index + 1)
        
        if self.connection.ValidPoint([prevPoint, pos, nextPoint]):
            old_len = len(self.connection.points)
            self.connection.InsertPoint(self.canvas, self.point, self.index)
            self.connection.ValidatePoints(self.canvas)
            if old_len == len(self.connection.points):
                self.enabled = False
            else:
                self.old_len = len(self.connection.points)

        else:
            self.enabled = False    
  
    def Undo(self):
        if self.old_len <= len(self.connection.points):
            self.connection.RemovePoint(self.canvas, self.index + 1, False)
        else: 
            pass

    def GetDescription(self):
        return _('Inserting point into %s connection ') %(self.connection.GetObject().GetType().GetId())
        