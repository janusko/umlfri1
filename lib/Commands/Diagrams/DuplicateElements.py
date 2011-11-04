from ..Base.Command import CCommand
from lib.Connections.Object import CConnectionObject
from lib.Drawing import Element
from lib.Exceptions import UMLException
from lib.Project import CProjectNode

class CDuplicateElementsCommand(CCommand):
    def __init__(self, elements, diagram):
        CCommand.__init__(self)
        self.__originalElements = elements
        self.__duplicatedElements = []
        self.__diagram = diagram
        self.__elementNodes = []

    def _Do(self):
        self.__diagram.DeselectAll()
        # create element objects
        newElementObjects = []
        for element in self.__originalElements:
            newElementobject = element.GetObject().Clone()
            newElementObjects.append(newElementobject)
        # create coresponding connection objects
        mapping = dict(zip((x.GetObject() for x in self.__originalElements), newElementObjects))
        parsed = set()
        for element in (x.GetObject() for x in self.__originalElements):
            for con in element.GetConnections():
                src, dest = con.GetSource(), con.GetDestination()
                if src in mapping:
                    src = mapping[src]
                if dest in mapping:
                    dest = mapping[dest]
                if src in parsed or dest in parsed:
                    continue
                newcon = CConnectionObject(con.GetType(), src, dest)
                newcon.GetDomainObject().CopyFrom(con.GetDomainObject())
                src.AddConnection(newcon)
                dest.AddConnection(newcon)
            parsed.add(mapping[element])
        # create elements
        backward_mapping = dict(zip(newElementObjects, self.__originalElements))
        try:
            for elobj in mapping.values():
                newElement = Element.CElement(self.__diagram, elobj)
                self.__diagram.AddToSelection(newElement)
                element = backward_mapping[elobj]
                newElement.CopyFromElement(element)
                #shift element +(5, 5) units
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
            self.__elementNodes.append(elementNode)
        del self.__originalElements

    def _Redo(self):
        self.__diagram.DeselectAll()
        for element in self.__duplicatedElements:
            self.__diagram.AddElement(element)
            self.__diagram.AddToSelection(element)
            elementNode = CProjectNode(self.__parentNode, element.GetObject())
            self.__parentNode.AddChild(elementNode)
            self.__elementNodes.append(elementNode)

    def _Undo(self):
        self.__diagram.DeselectAll()
        for element in self.__duplicatedElements:
            self.__diagram.DeleteElement(element)
        for elementNode in self.__elementNodes:
            self.__parentNode.RemoveChild(elementNode)
        self.__elementNodes = []


    def GetGuiUpdates(self):
        for element in self.__duplicatedElements:
            yield ('createElementObject', element.GetObject())
            yield ('elementChanged', (element, []))


    def __str__(self):
        return _('Duplicated %d elements in diagram %s') % \
               (len(self.__duplicatedElements), self.__diagram.GetName())
