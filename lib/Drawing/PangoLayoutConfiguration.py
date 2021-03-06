from lib.Depend.gtk2 import pango, gtk

fonts = {}

def ConfigurePangoLayout(layout, font):
    """
    Configures pango layout for specified font

    @param layout: Layout, which should be configured
    @type layout: L{Layout <pango.Layout>}

    @param font: Font, which should be used to configure Pango layout
    @type: font: L{CFont <lib.datatypes.CFont>}
    """
    
    resolution = gtk.gdk.screen_get_default().get_resolution()

    if resolution > 0:
        resolution_ratio = 96. / resolution
    else:
        resolution_ratio = 1
    
    fontHash = str(font)

    if fontHash in fonts:
        fontobj = fonts[fontHash]
    else:
        fonts[fontHash] = fontobj = pango.FontDescription()

        fontobj.set_family(font.GetFamily())
        fontobj.set_size(int(font.GetSize() * pango.SCALE * resolution_ratio))
        if 'bold' in font.GetStyle():
            fontobj.set_weight(pango.WEIGHT_BOLD)
        if 'italic' in font.GetStyle():
            fontobj.set_style(pango.STYLE_ITALIC)

    layout.set_font_description(fontobj)

    underline = 'underline' in font.GetStyle()
    strikeout = 'strike' in font.GetStyle()

    atlist = pango.AttrList()
    if underline:
        atlist.insert(pango.AttrUnderline(pango.UNDERLINE_SINGLE, 0, 10000))
    if strikeout:
        atlist.insert(pango.AttrStrikethrough(True, 0, 10000))

    layout.set_attributes(atlist)
