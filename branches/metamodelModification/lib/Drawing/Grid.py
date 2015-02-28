from lib.Base import CBaseObject
from lib.Drawing.Canvas.BufferCanvas import CBufferCanvas
from lib.config import config
from math import sqrt

class CGrid(CBaseObject):

    PAINT_METHOD_DEFAULT, \
    PAINT_METHOD_PATTERN = range(2)

    def __init__(self, local_settings=None):
        self.local_settings = bool(local_settings)
        self.UpdateState(local_settings)
        self.hor_spacing = 0
        self.ver_spacing = 0
        self.__paintMethod = self.PaintDefault
        #self.__paintMethod = self.PaintPattern
        if self.__paintMethod == self.PaintPattern:
            self.UpdatePattern()

    def UpdatePattern(self):
        """
        Redraws current grid pattern.
        Must be called to apply new grid settings.
        """
        if self.__paintMethod != self.PaintPattern:
            return
        # load grid appearance settings
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
            self.line_width = config['/Grid/LineWidth']
        fg1 = config['/Grid/LineColor1']
        fg2 = config["/Grid/LineColor2"]
        line_style1 = config['/Grid/LineStyle1']
        line_style2 = config['/Grid/LineStyle2']
        self.pattern_canvas = CBufferCanvas((self.hor_spacing, self.ver_spacing))
        # actual drawing
        if line_style1 != 'none':
            self.pattern_canvas.DrawLine((0.5, 0.5), (self.hor_spacing, 0.5), fg1,
                                                 self.line_width, line_style1)
            self.pattern_canvas.DrawLine((0.5, 0.5), (0.5, self.ver_spacing), fg1,
                                                 self.line_width, line_style1)
        if line_style2 != 'none':
            self.pattern_canvas.DrawLine((0.5, 0.5), (self.hor_spacing, 0.5), fg2,
                                                 self.line_width, line_style2)
            self.pattern_canvas.DrawLine((0.5, 0.5), (0.5, self.ver_spacing), fg2,
                                                 self.line_width, line_style2)

    def Paint(self, canvas, viewport):
        """
        Paints grid.

        @param canvas: Target canvas for drawing
        @type canvas: L{CCairoCanvas<CCairoCanvas>}

        @param viewport: Region of canvas where to draw grid.
         @type viewport: (tuple, tuple)
        """
        self.__paintMethod(canvas, viewport)

    def PaintDefault(self, canvas, viewport):
        """
        Paints grid directly on canvas.

        @param canvas: Target canvas for drawing
        @type canvas: L{CCairoCanvas<CCairoCanvas>}

        @param viewport: Region of canvas where to draw grid.
         @type viewport: (tuple, tuple)
        """
        # load grid appearance settings
        if not self.local_settings:
            self.visible = config['/Grid/Visible'] == 'true'
        if not self.visible:
            return
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
            self.line_width = config['/Grid/LineWidth']
        fg1 = config['/Grid/LineColor1']
        fg2 = config['/Grid/LineColor2']
        line_style1 = config['/Grid/LineStyle1']
        line_style2 = config['/Grid/LineStyle2']

        # region where grid will be drawn
        (x1, y1), (w, h) = viewport
        scale = canvas.GetScale()
        canvas.SetScale(1.0)
        hspace = self.hor_spacing * scale
        vspace = self.ver_spacing * scale
        x1 -= x1 * scale % hspace + .5
        y1 -= y1 * scale % vspace + .5
        x2 = x1 + w * scale
        y2 = y1 + h * scale

        #draw line_style1
        if not line_style1 == 'none':
            current = x1 + hspace
            while current <= x2:
                canvas.DrawLine((current, .5), (current, y2), fg1, self.line_width,
                    line_style1)
                current += hspace
            current = y1 + vspace
            while current <= y2:
                canvas.DrawLine((.5, current), (x2, current), fg1, self.line_width,
                    line_style1)
                current += vspace
        # draw line_style2
        if not line_style2 == 'none':
            current = x1 + hspace
            while current <= x2:
                canvas.DrawLine((current, .5), (current, y2), fg2, self.line_width,
                    line_style2)
                current += hspace
            current = y1 + vspace
            while current <= y2:
                canvas.DrawLine((.5, current), (x2, current), fg2, self.line_width,
                    line_style2)
                current += vspace
        canvas.SetScale(scale)

    def PaintPattern(self, canvas, viewport):
        """
        Paints the grid using buffered pattern.

        @param canvas: Target canvas for drawing
        @type canvas: L{CCairoCanvas<CCairoCanvas>}

        @param viewport: Region of canvas where to draw grid.
        @type viewport: (tuple, tuple)
        """
        if not self.local_settings:
            self.visible = config['/Grid/Visible'] == 'true'
        if not self.visible:
            return
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
        hspace = self.hor_spacing
        vspace = self.ver_spacing
        # region where pattern is applied
        x1 = -round(viewport[0][0] % hspace)
        y1 = -round(viewport[0][1] % vspace)
        x2 = x1 + viewport[1][0]
        y2 = y1 + viewport[1][1]
        x, y = x1, y1
        # pave the canvas with pattern
        while y < y2:
            while x < x2:
                canvas.DrawFromBuffer(self.pattern_canvas, (x, y), ((x, y), (x+hspace, y+vspace)))
                x += hspace
            x = x1
            y += vspace

    def SetPaintMethod(self, paintMethod):
        """
        Sets the way grid is painted.

        @param paintMethod: paint method id
        @type paintMethod: int
        """
        if paintMethod == self.PAINT_METHOD_DEFAULT:
            self.__paintMethod = self.PaintDefault
        elif paintMethod == self.PAINT_METHOD_PATTERN:
            self.__paintMethod = self.PaintPattern
        else:
            raise KeyError("Unknown paint method id: %s" % paintMethod)


    def UpdateState(self, data):
        """
        Update the state of the grid from local source.
        Curently not used.

        @param data: dictionary containing grid settings\
        @type data: dict
        """
        # local source of settings
        if self.local_settings:
            if not data: return
            self.local_settings = data['local']
            self.active = data['active']
            self.visible = data['visible']
            self.resize_elements = data['resize_elements']
            self.snap_breakpoints = data['snap_breakpoints']
            self.hor_spacing = data['hor_space']
            self.ver_spacing = data['ver_space']
            self.line_width = data['line_width']
            self.snap_mode = data['snap_mode']
            
    def GetState(self):
        """
        Get grid settings.

        @return: grid settings
        @rtype: dict
        """
        return  {'local': self.local_settings,
               'active': self.active,
               'visible': self.visible,
               'resize_elements': self.resize_elements,
               'snap_breakpoints': self.snap_breakpoints,
               'hor_space': self.hor_spacing,
               'ver_space': self.ver_spacing,
               'line_width': self.line_width,
               'snap_mode': self.snap_mode}
    
    def SnapPosition(self, pos):
        """
        Snap point position to grid.

        @param pos: point position
        @type pos: tuple

        @return: new position
        @rtype: tuple
        """
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
        x = self.hor_spacing * round(pos[0]/(float(self.hor_spacing)))
        y = self.ver_spacing * round(pos[1]/(float(self.ver_spacing)))
        return int(x), int(y)
    
    def SnapElement(self, element, pos, override=False):
        """
        Snaps element position according to snap mode on the grid.

        @param element: element to be snapped
        @type element: L{CElement<lib.Drawing.Element>}

        @param pos: position where element is moved
        @type pos: tuple

        @param override: ignore grid beiing turned off
        @type override: bool
        """
        if not self.local_settings:
            self.active = config['/Grid/Active'] == 'true'
            self.resize_elements = config['/Grid/ResizeElements'] == 'true'
            self.snap_mode = config['/Grid/SnapMode']
        if self.active or override:
            if self.resize_elements:
                self.ResizeElement(element)
            if self.snap_mode == 'TOP_LEFT':
                pos = self.SnapPosition(pos)
            elif self.snap_mode == 'CENTER':
                width, height = element.GetSize()
                center = (pos[0] + width/2.0, pos[1] + height/2.0)
                newCenter = self.SnapPosition(center)
                pos = (newCenter[0]-width/2.0, newCenter[1]-height/2.0)
            elif self.snap_mode == 'CORNERS':
                if not self.local_settings:
                    self.hor_spacing = config['/Grid/HorSpacing']
                    self.ver_spacing = config['/Grid/VerSpacing']
                w, h = element.GetSize()
                # finds out which element corner is nearest to grid
                top_left = list(pos)
                new_top_left = self.SnapPosition(top_left)
                len_top_left = sqrt((top_left[0] - new_top_left[0])**2 \
                    + (top_left[1] - new_top_left[1])**2)
                
                top_right = [top_left[0] + w, top_left[1]]
                new_top_right = self.SnapPosition(top_right)
                len_top_right = sqrt((top_right[0] - new_top_right[0])**2 \
                    + (top_right[1] - new_top_right[1])**2)
                
                bottom_left = [top_left[0], top_left[1] + h]
                new_bottom_left = self.SnapPosition(bottom_left)
                len_bottom_left = sqrt((bottom_left[0]-new_bottom_left[0])**2 \
                    + (bottom_left[1] - new_bottom_left[1])**2)
                
                bottom_right = [top_left[0] + w, top_left[1] + h]
                new_bottom_right = self.SnapPosition(bottom_right)
                len_bottom_right = sqrt((bottom_right[0]-new_bottom_right[0])**2\
                    + (bottom_right[1] - new_bottom_right[1])**2)
                
                minimum = min(len_top_left, len_top_right, 
                    len_bottom_right, len_bottom_left)
                if minimum==len_top_left:
                    pos = new_top_left
                elif minimum==len_top_right:
                    pos = (new_top_right[0] - w, new_top_right[1])
                elif minimum==len_bottom_left:
                    pos = (new_bottom_left[0], new_bottom_left[1] - h)
                else:
                    pos = (new_bottom_right[0] - w, new_bottom_right[1] - h)
        pos = (int(pos[0]), int(pos[1]))
        element.SetPosition(pos)
    
    def ResizeElement(self, element):
        """
        Resizes element to match grid spacing.
        Each corner is moved outwards to nearest grid intersection.

        @param element: element to resize
        @type element: L{CElement<lib.Drawing.Element>}
        """
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
        
        w, h = element.GetSize()
        minw, minh = element.GetMinimalSize()
        dw = -(w % self.hor_spacing)
        dh = -(h % self.ver_spacing)
        if minw > w + dw:
            dw = self.hor_spacing + dw
        if minh > h + dh:
            dh = self.ver_spacing + dh
        #rel = element.GetSizeRelative()
        #element.SetSizeRelative((rel[0] + dw, rel[1] + dh))
        element.SetSize((w + dw, h + dh))
        if self.snap_mode == 'CENTER':
            w, h = element.GetSize()
            dw = self.hor_spacing if w % (self.hor_spacing * 2) else 0
            dh = self.ver_spacing if h % (self.ver_spacing * 2) else 0
            if dw or dh:
                #rel = element.GetSizeRelative()
                #element.SetSizeRelative((rel[0] + dw, rel[1] + dh))
                element.SetSize((w + dw, h + dh))
        
    def SnapConnection(self, conn, pos, idx, override=False):
        """
        Snap connection breakpoint to grid.

        @param conn: connection object
        @type conn: L{CConnection<lib.Drawing.Connection>}

        @param pos: pos where connection point is moved
        @type pos: tuple

        @param idx: connection breakpoint index
        @type idx: int

        @param override: ignore grid beiing turned off
        @type override: bool
        """
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
            self.snap_breakpoints = config['/Grid/SnapBreakpoints'] == 'true'
            self.active = config['/Grid/Active'] == 'true'
        if (self.active and self.snap_breakpoints) or override:
            pos = self.SnapPosition(pos)
        conn.MovePoint(pos, idx)
    
    def IsActive(self):
        """
        Is grid active (whether elements and element connections will be snapped to grid).

        @return: is grid active
        @type: bool
        """
        if not self.local_settings:
            self.active = config['/Grid/Active'] == 'true'
        return self.active
        
    def IsVisible(self):
        """
        Whether grid will be drawn on canvas.

        @return: is grid visible
        @rtype: bool
        """
        if not self.local_settings:
            self.visible = config['/Grid/Visible'] == 'true'
        return self.visible
    
