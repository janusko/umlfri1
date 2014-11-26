from ..Base.Command import CCommand
from lib.Connections.Object import CConnectionObject
from lib.Drawing.Connection import CConnection

class CMoveElementCommand(CCommand):
    def __init__(self, elementVisual, position):
        CCommand.__init__(self)
        
        self.__elementVisual = elementVisual
        self.__newPosition = position
        self.__oldPosition = None
    
    def _Do(self):
        self.__oldPosition = self.__elementVisual.GetPosition()
        self.__elementVisual.SetPosition(self.__newPosition)
    
    def _Redo(self):
        self.__elementVisual.SetPosition(self.__newPosition)
    
    def _Undo(self):
        self.__elementVisual.SetPosition(self.__oldPosition)

    def GetGuiUpdates(self):
        return [
            ('elementChanged', (self.__elementVisual, []))
        ]
    
    def __str__(self):
        return _("Element %s was moved") % (
            self.__elementVisual.GetObject().GetName()
        )
