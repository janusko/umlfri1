from ..Base.Command import CCommand
from lib.Drawing import Element
from lib.Exceptions import UMLException
from lib.Project import CProjectNode

class CDuplicateElementsCommand(CCommand):
    def __init__(self, elements, diagram):
        CCommand.__init__(self)

        self.__originalElements = elements
        self.__duplicatedElements = []
        self.__diagram = diagram

    def _Do(self):
        self.__diagram.DeselectAll()
        try:
            for element in self.__originalElements:
                newElementobject = element.GetObject().Clone()
                newElement = Element.CElement(self.__diagram, newElementobject)
                self.__diagram.AddToSelection(newElement)
                newElement.CopyFromElement(element)
                # shift element +(5, 5) units
                newElement.SetPosition(map(sum, zip(newElement.GetPosition(), (5.0, 5.0))))
                self.__duplicatedElements.append(newElement)
        except UMLException, e:
            for el in self.__duplicatedElements:
                self.__diagram.DeleteElement(el)
            raise
        self.__parentNode = self.__diagram.GetNode()
        for element in self.__duplicatedElements:
            elementNode = CProjectNode(self.__parentNode, element.GetObject())
            self.__parentNode.AddChild(elementNode)

    def _Redo(self):
        for element in self.__duplicatedElements:
            diagram.AddElement(element)
            elementNode = CProjectNode(self.__parentNode, element.GetObject())
            self.__parentNode.Add(Child)

    def _Undo(self):
        for element in self.__duplicatedElements:
            self.__diagram.DeleteElement(element)
            self.__parentNode.RemoveChild(element.GetObject())

    def GetGuiUpdates(self):
        for element in self.__duplicatedElements:
            yield ('createElementObject', element.GetObject())
            yield ('elementChanged', (element, []))


    def __str__(self):
        return _('Duplicated %d elements in diagram %s') % \
               (len(self.__duplicatedElements), self.__diagram.GetName())
