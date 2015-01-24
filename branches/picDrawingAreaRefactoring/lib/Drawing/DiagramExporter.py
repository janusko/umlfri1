from lib.Drawing.Canvas import CExportCanvas


class CDiagramExporter():

    def __init__(self, storage, export_type):
        """
        Creates new L{CDiagramExporter<DiagramExporter.CDiagramExporter>} with specified storage and export type.

        @param storage: Metamodel storage
        @type storage : L{AbstractStorage<lib.Storages.CAbstractStorage>}
        @param export_type: Export type. One of "png", "pdf", "svg", "ps", "pixbuf"
        """
        self.storage = storage
        self.export_type = export_type
        self.zoom = 1.0
        self.padding = 0
        self.background = None

    def Export(self, diagram, filename):
        """
        Exports specified diagram to file.

        @param diagram: Diagram to export
        @type diagram : L{CDiagram<Diagram.CDiagram>}

        @param filename: Path of the file, where to export the diagram.
        @type filename : str
        """
        diagram.GetSelection().DeselectAll()

        (x1, y1), (x2, y2) = diagram.GetSizeSquare()
        sizeX = x2 - x1
        sizeY = y2 - y1
        x = x1
        y = y1

        sizeX = (sizeX + self.padding * 2) * self.zoom
        sizeY = (sizeY + self.padding * 2) * self.zoom
        canvas = CExportCanvas(self.storage, self.export_type,
                               filename, sizeX, sizeY, background = self.background)
        canvas.SetScale(self.zoom)
        canvas.MoveBase(x - self.padding, y - self.padding)
        diagram.PaintFull(canvas)
        canvas.Finish()

    def GetBackground(self):
        """
        Returns background color of exported diagram.

        @rtype : L{CColor<lib.datatypes.CColor>}
        @return: Background color of exported diagram.
        """
        return self.background

    def SetBackground(self, background):
        """
        Sets background color of exported diagram

        @type background : L{CColor<lib.datatypes.CColor>}
        @param background: Background color of exported diagram.
        """
        self.background = background

    def GetZoom(self):
        """
        Returns zoom of exported diagram.

        @rtype : float
        @return: Zoom of the exported diagram.
        """
        return self.zoom

    def SetZoom(self, zoom):
        """
        Sets zoom of the exported diagram.

        @param zoom: Zoom of the exported diagram.
        @type zoom : float
        """
        self.zoom = zoom

    def GetPadding(self):
        """
        Gets the padding of the exported diagram.

        @rtype : int
        @return: Padding of the exported diagram.
        """
        return self.padding

    def SetPadding(self, padding):
        """
        Sets padding of the diagram.

        @param padding: Padding of the diagram.
        @type padding : int
        """
        self.padding = padding