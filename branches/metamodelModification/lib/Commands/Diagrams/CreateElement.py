from ..Base.Command import CCommand
from lib.Drawing import CElement
from lib.Elements import CElementObject
from lib.Elements.TypeValidator import CElementTypeValidator
from lib.Project import CProjectNode

class CCreateElementCommand(CCommand):
    def __init__(self, elementType, diagram):
        CCommand.__init__(self)

        self.__elementType = elementType
        self.__diagram = diagram
        self.__parentNode = None
        self.__elementObject = None
        self.__elementNode = None
        self.__elementVisual = None

        CElementTypeValidator().CanCreateElementAsChild(elementType, diagram.GetNode())


    def _Do(self):
        self.__parentNode = self.__diagram.GetNode()
        self.__elementObject = CElementObject(self.__elementType)
        self.__elementVisual = CElement(self.__diagram, self.__elementObject)

        self.__elementNode = CProjectNode(self.__parentNode, self.__elementObject)
        self.__parentNode.AddChild(self.__elementNode)

    def _Redo(self):
        self.__elementNode = CProjectNode(self.__parentNode, self.__elementObject)
        self.__parentNode.AddChild(self.__elementNode)
        self.__diagram.AddElement(self.__elementVisual)

    def _Undo(self):
        for diagram in self.__elementObject.GetAppears():
            diagram.DeleteItem(diagram.GetElement(self.__elementObject))

        self.__parentNode.RemoveChild(self.__elementNode)
        self.__elementNode = None

    def GetGuiUpdates(self):
        return [
            ('createElementObject', self.__elementObject),
            ('elementChanged', (self.__elementVisual, []))
        ]

    def __str__(self):
        return _('Element %s created in diagram %s') % (self.__elementType.GetId(), self.__diagram.GetName())

    def GetElementObject(self):
        return self.__elementObject

    def GetElementVisual(self):
        return self.__elementVisual
