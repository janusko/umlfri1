from ..Base.Command import CCommand
from lib.Elements.Object import CElementObject
from lib.Project.ProjectNode import CProjectNode

class CCreateElementObjectCommand(CCommand):
    def __init__(self, elementType, parentNode):
        CCommand.__init__(self)
        
        self.__elementType = elementType
        self.__parentNode = parentNode
        self.__elementObject = None
        self.__elementNode = None
    
    def _Do(self):
        self.__elementObject = CElementObject(self.__elementType)

        self._Redo()
    
    def _Redo(self):
        self.__elementNode = CProjectNode(self.__parentNode, self.__elementObject)
        self.__parentNode.AddChild(self.__elementNode)
    
    def _Undo(self):
        for diagram in self.__elementObject.GetAppears():
            diagram.DeleteItem(diagram.GetElement(self.__elementObject))
        
        self.__parentNode.RemoveChild(self.__elementNode)
        self.__elementNode = None
    
    def GetGuiUpdates(self):
        return [
            ('createElementObject', self.__elementObject)
        ]
    
    def __str__(self):
        return _('Element %s created in the project') % self.__elementType.GetId()
    
    def GetElementObject(self):
        return self.__elementObject
