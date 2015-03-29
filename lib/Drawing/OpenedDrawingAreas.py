from lib.Drawing.DrawingArea import CDrawingArea


class COpenedDrawingAreas:
    "Tu je pojde komentar triedy..."

    def __init__(self, app):
        """
        Creates new instance.
        """
        self.application = app
        self.diagrams = dict()
        """Dict of opened drawing Areas. Key = Diagram, Value = DrawingArea."""
        self.activeDiagram = None
        """Active diagram."""

    def GetDrawingArea(self, diagram):
        """
        Returns instance of CDrawingArea, that belongs to diagram in param.
        :param diagram:
        :return:
        """
        if diagram in self.diagrams:
            return self.diagrams[diagram]

    def __AddDiagram(self, diagram):
        """
        Adds diagram into dict and creates CDrawingArea for him.
        :param diagram:
        :return:
        """
        drawing_area = CDrawingArea(self.application, diagram)
        self.diagrams[diagram] = drawing_area

    def SetActiveDiagram(self, diagram):
        """
        Sets diagram in param to current diagram.
        :param diagram:
        :return:
        """
        if diagram not in self.diagrams:
            self.__AddDiagram(diagram)
        self.activeDiagram = diagram

    def GetActiveDiagram(self):
        """
        Returns active diagram.
        :return:
        """
        return self.activeDiagram

    def GetActiveDrawingArea(self):
        """
        Returns active drawing area.
        :return:
        """
        if self.activeDiagram is not None and self.activeDiagram in self.diagrams:
            return self.diagrams[self.activeDiagram]