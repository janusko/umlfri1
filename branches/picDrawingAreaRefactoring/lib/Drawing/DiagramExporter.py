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

    def ExportDiagram(self, diagram, filename):
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

    def GetSelectionPixbuf(self, diagram):
        """
        Creates pixbuf, which contains exported diagram with only selected elements and connections.

        @param diagram: Diagram to export
        @type diagram : L{CDiagram<Diagram.CDiagram>}

        @return: Pixbuf containing exported diagram with selected elements and connections.
        """
        pos, (sizeX, sizeY) = diagram.GetSelectSquare(True)
        (sizeX, sizeY) = self.__CalculateDiagramPhysicalSize((sizeX, sizeY))
        canvas = self.__CreateCanvas('pixbuf', None, (sizeX, sizeY), pos)
        diagram.PaintSelected(canvas)
        return canvas.Finish()

    def __CreateCanvas(self, export_type, filename, (sizeX, sizeY), offset):
        """
        Creates and configures export canvas.

        @param export_type: Type of exported format.
        @param filename: Filename of exported file.
        @param offset: Offset of the canvas.
        @rtype : L{CCairoBaseCanvas<Canvas.CairoBase.CCairoBaseCanvas>}
        @return: Configured canvas.
        """
        canvas = CExportCanvas(self.storage, 'pixbuf',
                               None, sizeX, sizeY, background = self.background)
        canvas.SetScale(self.zoom)
        self.__SetCanvasOffset(canvas, offset)
        return canvas

    def __CalculateDiagramPhysicalSize(self, logicalSize):
        """
        Calculates diagram's physical size from its logical size. Applies zoom and padding.

        @param logicalSize: Logical size of diagram.
        @type logicalSize : tuple

        @rtype : tuple
        @return: Diagram's physical size with applied zoom and padding.
        """
        (sizeX, sizeY) = logicalSize
        sizeX = (sizeX + self.padding * 2) * self.zoom
        sizeY = (sizeY + self.padding * 2) * self.zoom
        return (sizeX, sizeY)

    def __SetCanvasOffset(self, canvas, (x, y)):
        """
        Adjust offset of an canvas with specified position and padding.

        @param canvas: Canvas, which offset should be set.
        @type  canvas: L{CCairoBaseCanvas<Canvas.CairoBase.CCairoBaseCanvas>}
        """
        canvas.MoveBase(x - self.padding, y - self.padding)

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