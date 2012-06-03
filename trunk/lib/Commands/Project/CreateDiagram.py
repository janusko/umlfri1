from ..Base.Command import CCommand
from lib.Drawing import CDiagram

class CCreateDiagramCommand(CCommand):
    def __init__(self, diagramType, parentNode):
        CCommand.__init__(self)
        
        self.__diagram = None
        self.__diagramType = diagramType
        self.__parentNode = parentNode

    def _Do(self):
        self.__diagram = CDiagram(self.__diagramType)
        
        self._Redo()
    
    def _Undo(self):
        self.__parentNode.RemoveDiagram(self.__diagram)
    
    def _Redo(self):
        self.__parentNode.AddDiagram(self.__diagram)
    
    def GetGuiUpdates(self):
        return [
            ('createDiagram', self.__diagram)
        ]
    
    def GetGuiActions(self):
        return [
            ('expandNode', self.__parentNode),
            ('openDiagram', self.__diagram)
        ]
    
    def __str__(self):
        return _("%s added to the project") % self.__diagramType.GetId()
    
    def GetDiagram(self):
        return self.__diagram
