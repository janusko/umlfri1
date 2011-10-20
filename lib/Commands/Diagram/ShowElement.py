from ..Base.Command import CCommand
from lib.Drawing import CElement

class CShowElementCommand(CCommand):
    def __init__(self, elementObject, diagram):
        CCommand.__init__(self)
        
        self.__elementObject = elementObject
        self.__diagram = diagram
        self.__elementVisual = None
    
    def _Do(self):
        self.__elementVisual = CElement(self.__diagram, self.__elementObject)
    
    def _Redo(self):
        self.__diagram.AddElement(self.__elementVisual)
    
    def _Undo(self):
        self.__diagram.DeleteElement(self.__elementVisual)
    
    def GetGuiUpdates(self):
        return [
            ('elementChanged', (self.__elementVisual, []))
        ]

    def GetElementVisual(self):
        return self.__elementVisual
