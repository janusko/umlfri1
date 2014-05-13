from lib.Depend.gtk2 import pango
from lib.Depend.gtk2 import pangocairo
from lib.Depend.gtk2 import cairo

from lib.Exceptions.UserException import *
from Abstract import CAbstractCanvas

from ..PangoLayoutConfiguration import ConfigurePangoLayout

#  dash sequence for line styles used in self.cr.set_dash(dash_sequence, offset), where
#  dash_sequence - an array specifying alternate lengths of on and off stroke portions
#  offset - an offset into the dash pattern at which the stroke should start
LINE_STYLES = {'solid': [],
               'dot': [2,2],
               'doubledot': [8,2,2,2]}

pixmaps = {}

def PixmapFromPath(storage, path):
    if (storage, path) in pixmaps:
        tmp = pixmaps[(storage, path)]
    else:
        if storage is None:
            pathx = path
        else:
            pathx = storage.file(path)

        tmp = cairo.ImageSurface.create_from_png(pathx)
        pixmaps[(storage, path)] = tmp

    return tmp

def HexToRGB(hexcolor):
    #converts Hex colors(HTML format) to RGB, used to set fg, bg, font color

    #if not hexcolor[0] == '#': # if hexcolor is a word 
    #    hexcolor = colors.colors[hexcolor]
    #hexcolor = hexcolor.strip()
    #hexcolor = hexcolor[1:]
    #if len(hexcolor) != 6:
    #    raise DrawingError('Invalid hex color, use #RRGGBB format or color name.')
    #r, g, b = hexcolor[:2], hexcolor[2:4], hexcolor[4:]
    #r, g, b = [int(n, 16) for n in (r, g, b)]
    r, g, b = hexcolor.GetRed(), hexcolor.GetGreen(), hexcolor.GetBlue()
    return float(r)/255, float(g)/255, float(b)/255

class CCairoBaseCanvas(CAbstractCanvas):
    def __init__(self, cairo_context, storage = None):
        self.cairo_context = cairo_context
        self.alpha = 1.0
        self.scale = 1.0
        self.storage = storage
        self.cr = pangocairo.CairoContext(self.cairo_context)
        self.fonts = {}
        
        self.baseX = 0
        self.baseY = 0

    def ToLogical(self, pos):
        pos = (int((pos[0] - self.baseX)/self.scale),int((pos[1] - self.baseY)/self.scale))
        return pos

    def ToPhysical(self, pos):
        pos = (int(pos[0]*self.scale + self.baseX),int(pos[1]*self.scale + self.baseY))
        return pos

    def SetScale(self, scale):
        self.scale = scale

    def GetScale(self):
        return float(self.scale)
    
    def MoveBase(self, x, y):
        self.baseX = x
        self.baseY = y

    def SetAlpha(self, alpha):
        if alpha >= 0.0 and alpha <= 1.0:
            self.alpha = alpha

    def __SetFont(self, font):
        pango_layout = self.cr.create_layout()

        ConfigurePangoLayout(pango_layout, font)
        
        return pango_layout

    def DrawArc(self, pos, size, arc = (0, 360), fg = None, bg = None, line_width = None, line_style = None):
        self.cr.save()

        if int(size[0]) < int(size[1]):
            size1=1.0
            size0=float(size[0])/float(size[1])
            radius = int(size[1])/2

        elif int(size[0]) == int(size[1]):
            size0=1.0
            size1=1.0
            radius = int(size[1])/2
        else:
            size0=1.0
            size1=float(size[1])/float(size[0])
            radius = int(size[0])/2
            
        self.cr.scale(self.scale, self.scale)
        self.cr.translate (int(pos[0] - self.baseX)+(int(size[0])/2), int(pos[1] - self.baseY)+(int(size[1])/2))
        self.cr.scale(size0, size1)
        self.cr.arc(0,0,radius,arc[0],arc[1])

        if bg is not None:
            temp_color = HexToRGB(bg)
            self.cr.set_source_rgba(temp_color[0], temp_color[1], temp_color[2], self.alpha)
            self.cr.fill_preserve()

        if fg is not None:
            temp_color = HexToRGB(fg)
            self.cr.set_source_rgba(temp_color[0], temp_color[1], temp_color[2], self.alpha)

        if line_width is not None:
            self.cr.set_line_width(line_width)

        if line_style is not None:
            self.cr.set_dash(LINE_STYLES[line_style], 0)       

        self.cr.stroke()
        self.cr.restore()

    def DrawLine(self, start, end, fg, line_width = None, line_style = None):
        self.cr.save()
        self.cr.scale(self.scale, self.scale)
        self.cr.move_to(float(start[0] - self.baseX),float(start[1] - self.baseY))
        self.cr.line_to(float(end[0] - self.baseX),float(end[1] - self.baseY))

        if fg is not None: 
            temp_color = HexToRGB(fg)
            self.cr.set_source_rgba(temp_color[0], temp_color[1], temp_color[2], self.alpha)

        if line_width is not None:
            self.cr.set_line_width(line_width)

        if line_style is not None:
            self.cr.set_dash(LINE_STYLES[line_style], 0)

        self.cr.stroke()
        self.cr.restore()

    def __DrawPolyAll(self, points, fg, bg, line_width, line_style, closed):
        self.cr.save()
        self.cr.scale(self.scale, self.scale)
        move_pen = True

        for x,y in points :
            if move_pen:
                self.cr.move_to(x - self.baseX,y - self.baseY)
                move_pen = False
            self.cr.line_to(x - self.baseX,y - self.baseY)

        if closed:
            self.cr.close_path()

        if bg is not None:
            temp_color = HexToRGB(bg)
            self.cr.set_source_rgba(temp_color[0], temp_color[1], temp_color[2], self.alpha)
            self.cr.fill_preserve()

        if fg is not None:
            temp_color = HexToRGB(fg)
            self.cr.set_source_rgba(temp_color[0], temp_color[1], temp_color[2], self.alpha)

        if line_width is not None:
            self.cr.set_line_width(line_width)

        if line_style is not None:
            self.cr.set_dash(LINE_STYLES[line_style], 0)

        self.cr.stroke()
        self.cr.restore()

    def DrawLines(self, points, fg, line_width = None, line_style = None):
        self.__DrawPolyAll(points, fg, None, line_width, line_style, False)

    def DrawPolygon(self, points, fg = None, bg = None, line_width = None, line_style = None):
        self.__DrawPolyAll(points, fg, bg, line_width, line_style, True)

    def DrawPath(self, path, fg = None, bg = None, line_width = None, line_style = None):
        for single in path:
            t = single.GetType()
            if t == 'polygon':
                self.DrawPolygon(single, fg, bg, line_width, line_style)
            elif t == 'polyline':
                self.DrawLines(single, fg, line_width, line_style)

    def DrawRectangle(self, pos, size, fg = None, bg = None, line_width = None, line_style = None):
        self.cr.save()
        self.cr.scale(self.scale, self.scale)
        self.cr.rectangle(int(pos[0] - self.baseX), int(pos[1] - self.baseY), int(size[0]), int(size[1]))

        if bg is not None:
            temp_color = HexToRGB(bg)
            self.cr.set_source_rgba(temp_color[0], temp_color[1], temp_color[2], self.alpha)
            self.cr.fill_preserve()

        if fg is not None:
            temp_color = HexToRGB(fg)
            self.cr.set_source_rgba(temp_color[0], temp_color[1], temp_color[2], self.alpha)

        if line_width is not None:
            self.cr.set_line_width(line_width)

        if line_style is not None:
            self.cr.set_dash(LINE_STYLES[line_style], 0)

        self.cr.stroke()
        self.cr.restore()

    def DrawText(self, pos, text, font, fg):
        self.cr.save()
        self.cr.scale(self.scale, self.scale)
        pango_layout = self.__SetFont(font)
        self.cr.move_to (int(pos[0] - self.baseX), int(pos[1] - self.baseY))
        pango_layout.set_text(text)
        font_color = HexToRGB(fg)
        self.cr.set_source_rgb(font_color[0], font_color[1], font_color[2])
        self.cr.show_layout(pango_layout)
        self.cr.stroke ()
        self.cr.restore()

    def GetTextSize(self, text, font):
        pango_layout = self.__SetFont(font)
        pango_layout.set_text(text)
        return int(pango_layout.get_size()[0]/float(pango.SCALE)), int(pango_layout.get_size()[1]/float(pango.SCALE))

    #obsolete, gets font base line, used by CSvgCanvas class to export to svg
    def GetFontBaseLine(self, font):
        lines = self.pango_layout.get_iter()
        baseline = lines.get_baseline()/pango.SCALE
        return baseline

    def DrawPixbuf(self, pixbuf, pos):
        self.cairo_context.save()
        self.cairo_context.scale(self.scale, self.scale)
        self.cairo_context.set_source_pixbuf(pixbuf, pos[0] - self.baseX, pos[1] - self.baseY)
        self.cairo_context.paint()
        self.cairo_context.restore()

    def DrawIcon(self, pos, filename):
        if self.storage is None:
            raise DrawingError('storage')
        pixmap = PixmapFromPath(self.storage, filename)
        self.cr.save()
        self.cr.scale(self.scale, self.scale)
        self.cr.set_source_surface (pixmap, pos[0] - self.baseX, pos[1] - self.baseY)
        self.cr.paint()
        self.cr.restore()

    def DrawFromBuffer(self, buffer, origin, region):
        """
        Draws contents of buffer onto canvas.

        @param buffer: BufferCanvas containig pattern/image...
        @type buffer: L{CBufferCanvas <lib.Drawing.Canvas.BufferCanvas.CBufferCanvas>}

        @param origin: coordinate at which the surface origin should appear
        @type: tuple

        @param region: rectangular region on target canvas to be filled with buffer canvas
        @type region: (tuple, tuple)
        """
        self.cr.save()
        self.cr.scale(self.scale, self.scale)
        surface = buffer.GetSurface()
        self.cr.set_source_surface(surface, *origin)
        self.cr.rectangle(region[0][0], region[0][1], region[1][0], region[1][1])
        self.cr.fill()
        self.cr.restore()

    def GetIconSize(self, filename):
        if self.storage is None:
            raise DrawingError('storage')
        pixmap = PixmapFromPath(self.storage, filename)
        return pixmap.get_width(), pixmap.get_height() # + self.cr.scale(self.scale, self.scale)
