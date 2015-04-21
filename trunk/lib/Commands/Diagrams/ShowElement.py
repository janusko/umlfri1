from ..Base.Command import CCommand
from lib.Drawing import CElement

class CShowElementCommand(CCommand):
    def __init__(self, elementObject, diagram, selection):
        CCommand.__init__(self)
        
        self.__elementObject = elementObject
        self.__diagram = diagram
        self.__elementVisual = None
        self.__selection = selection
    
    def _Do(self):
        self.__elementVisual = CElement(self.__diagram, self.__elementObject)
    
    def _Redo(self):
        self.__diagram.AddElement(self.__elementVisual)
    
    def _Undo(self):
        self.__diagram.DeleteElement(self.__elementVisual, self.__selection)
    
    def GetGuiUpdates(self):
        return [
            ('elementChanged', (self.__elementVisual, []))
        ]
    
    def __str__(self):
        return _("Element %s is shown on diagram %s") % (
            self.__elementObject.GetName(),
            self.__diagram.GetName()
        ) 

    def GetElementVisual(self):
        return self.__elementVisual
