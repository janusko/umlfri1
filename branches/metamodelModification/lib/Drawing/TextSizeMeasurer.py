from lib.Depend.gtk2 import pango
from lib.Depend.gtk2 import gtk

from PangoLayoutConfiguration import ConfigurePangoLayout

class TextSizeMeasurer:
    """
    Measures text size using Pango layout
    """

    def __init__(self):
        self.pango_context = gtk.gdk.pango_context_get()


    def MeasureSize(self, text, font):
        """
        Measures text size using specified font. Returns tuple with text dimensions.

        @param text: Text, which size should be measured
        @type text: str

        @param font: Font, which the text should be measured with
        @type: font: L{CFont <lib.datatypes.CFont>}
        """
        pango_layout = pango.Layout(self.pango_context)
        ConfigurePangoLayout(pango_layout, font)

        pango_layout.set_text(text)

        return pango_layout.get_pixel_size()

