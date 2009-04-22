# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation



class CInsertConnectionPointCmd(CHistoryOperation):

    def __init__(self, DragPoint, canvas, point, description = None): 
        CHistoryOperation.__init__(self, description) 
        self.connection, self.index = DragPoint
        self.canvas = canvas
        self.point = point


    def do (self):
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
                if self.description == None:
                    self.description = _('Insert point to %s connection ') %(self.connection.GetObject().GetType().GetId())
        else:
            self.enabled = False    
  
  
    def undo(self):
        if self.old_len <= len(self.connection.points):
            self.connection.RemovePoint(self.canvas, self.index + 1, False)
        else: 
            pass
  
    def redo(self):
        self.do()


    def isEnabled(self):
        return self.enabled


