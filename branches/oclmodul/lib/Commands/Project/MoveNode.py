from ..Base.Command import CCommand, CommandNotDone

class CMoveNodeCommand(CCommand):
    def __init__(self, node, newParent, newPosition):
        CCommand.__init__(self)
        
        self.__node = node
        self.__newParent = newParent
        self.__newPosition = newPosition
        self.__oldParent = None
        self.__oldPosition = None
    
    def _Do(self):
        if self.__newParent is None:
            raise CommandNotDone # TODO: more verbose error
        
        self.__oldParent = self.__node.GetParent()
        
        if self.__oldParent is None:
            raise CommandNotDone # TODO: more verbose error
        
        self.__oldPosition = self.__oldParent.GetChildIndex(self.__node)
        
        if self.__oldParent is self.__newParent and self.__oldPosition == self.__newPosition:
            raise CommandNotDone
        
        parent = self.__newParent
        while parent is not None:
            if parent is self.__node:
                raise CommandNotDone # TODO: more verbose error
            parent = parent.GetParent()
        
        self._Redo()
    
    def _Redo(self):
        self.__oldParent.RemoveChild(self.__node)
        self.__newParent.AddChild(self.__node, pos = self.__newPosition)
    
    def _Undo(self):
        self.__newParent.RemoveChild(self.__node)
        self.__oldParent.AddChild(self.__node, pos = self.__oldPosition)
    
    def GetGuiUpdates(self):
        return [
            ('moveNodeInProject', (self.__node, self.__oldParent, self.__newParent))
        ]
    
    def __str__(self):
        return _("Element %s moved in project tree") % (self.__node.GetName())
