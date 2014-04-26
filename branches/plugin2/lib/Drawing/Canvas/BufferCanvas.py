import cairo
import gtk
from lib.Drawing.Canvas.CairoBase import CCairoBaseCanvas

class CBufferCanvas(CCairoBaseCanvas):
    """
    Buffer canvas for storing patterns/objects intended to be drawn on
    main canvas.
    """
    def __init__(self, size, storage=None):
        self.Resize(size)
        CCairoBaseCanvas.__init__(self, self.cairo_context, storage)

    def GetSurface(self):
        """
        Returns target surface.
        """
        return self.surface

    def Resize(self, size):
        """
        Resizes buffer.

        @param size: 2D size to be allocated
        @type size: tuple
        """
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *size)
        self.cairo_context = cairo.Context(self.surface)

    def Clear(self):
        """
        Clears buffer.
        """
        self.cr.save()
        self.cr.set_operator(cairo.OPERATOR_CLEAR)
        self.cr.rectangle(.0, .0, surface.width, surface.heigth)
        self.cr.fill()
        self.cr.restore()