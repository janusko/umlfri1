from lib.Commands import CBaseCommand


class CMoveConnectionPointCmd(CBaseCommand):
    def __init__(self, connection, index, canvas, point): 
        CBaseCommand.__init__(self) 
        self.connection = connection
        self.index = index
        self.canvas = canvas
        self.point = point
        self.enabled = True

    def Do(self):
        self.old_point = self.connection.GetPoint(self.canvas, self.index)
        self.old_len = len(self.connection.points)
        self.connection.MovePoint(self.canvas, self.point, self.index)

    def Undo(self):
        if self.old_len > len(self.connection.points) :
            self.connection.InsertPoint(self.canvas, self.old_point, self.index - 1)  
            self.insertedPoint = True
        else:
            self.connection.MovePoint(self.canvas, self.old_point, self.index)
            self.insertedPoint = False

    def Redo(self):
        if self.insertedPoint:
            self.connection.RemovePoint(self.canvas, self.index)  
        else:
            self.connection.MovePoint(self.canvas, self.point, self.index)

    def GetDescription(self):
        return _('Moving %s connection point') %(self.connection.GetObject().GetType().GetId())
