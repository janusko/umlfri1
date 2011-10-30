from ..Base.Command import CCommand, CommandNotDone

class CMoveDiagramCommand(CCommand):
    def __init__(self, diagram, newParent, newPosition):
        CCommand.__init__(self)
        
        self.__diagram = diagram
        self.__newParent = newParent
        self.__newPosition = newPosition
        self.__oldParent = None
        self.__oldPosition = None
    
    def _Do(self):
        if self.__newParent is None:
            raise CommandNotDone # TODO: more verbose error
        
        self.__oldParent = self.__diagram.GetNode()
        self.__oldPosition = self.__oldParent.GetDiagramIndex(self.__diagram)
        
        if self.__oldParent is self.__newParent and self.__oldPosition == self.__newPosition:
            raise CommandNotDone
        
        self._Redo()
    
    def _Redo(self):
        self.__oldParent.RemoveDiagram(self.__diagram)
        self.__newParent.AddDiagram(self.__diagram, pos = self.__newPosition)
    
    def _Undo(self):
        self.__newParent.RemoveChild(self.__diagram)
        self.__oldParent.AddChild(self.__diagram, pos = self.__oldPosition)
    
    def GetGuiUpdates(self):
        return [
            ('moveDiagramInProject', (self.__diagram, self.__oldParent, self.__newParent))
        ]
    
    def __str__(self):
        return _("Diagram %s moved in project tree") % (self.__diagram.GetName())
