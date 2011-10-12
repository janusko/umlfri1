from lib.Base import CBaseObject
from lib.Drawing.Canvas.BufferCanvas import CBufferCanvas
from lib.config import config
from math import sqrt

class CGrid(CBaseObject):
    
    def __init__(self, local_settings=None):
        self.local_settings = bool(local_settings)
        self.UpdateState(local_settings)
        self.hor_spacing = 0
        self.ver_spacing = 0
        self.__CreatePattern()

    def __CreatePattern(self):
        """
        Redraws current grid pattern.
        """
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

    def PaintPattern(self, canvas, viewport):
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
        # pave the region with pattern
        while y < y2:
            while x < x2:
                canvas.DrawFromBuffer(self.pattern_canvas, (x, y), ((x, y), (x+hspace, y+vspace)))
                x += hspace
            x = x1
            y += vspace




    def UpdateState(self, data):
        '''
        Update the state of the grid from local source.
        '''
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
        ret = {'local': self.local_settings,
               'active': self.active,
               'visible': self.visible,
               'resize_elements': self.resize_elements,
               'snap_breakpoints': self.snap_breakpoints,
               'hor_space': self.hor_spacing,
               'ver_space': self.ver_spacing,
               'line_width': self.line_width,
               'snap_mode': self.snap_mode}
        return ret
    
    def SnapPosition(self, pos):
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
        x = self.hor_spacing * round(pos[0]/(float(self.hor_spacing)))
        y = self.ver_spacing * round(pos[1]/(float(self.ver_spacing)))
        return x, y
    
    def SnapElement(self, element, pos, canvas, override=False):
        '''
        Snaps element position according to snap mode.
        '''
        if not self.local_settings:
            self.active = config['/Grid/Active'] == 'true'
            self.resize_elements = config['/Grid/ResizeElements'] == 'true'
            self.snap_mode = config['/Grid/SnapMode']
        if self.active or override:
            if self.resize_elements:
                self.ResizeElement(element, canvas)
            if self.snap_mode == 'TOP_LEFT':
                pos = self.SnapPosition(pos)
            elif self.snap_mode == 'CENTER':
                width, height = element.GetSize(canvas)
                center = (pos[0] + width/2.0, pos[1] + height/2.0)
                newCenter = self.SnapPosition(center)
                pos = (newCenter[0]-width/2.0, newCenter[1]-height/2.0)
            elif self.snap_mode == 'CORNERS':
                if not self.local_settings:
                    self.hor_spacing = config['/Grid/HorSpacing']
                    self.ver_spacing = config['/Grid/VerSpacing']
                w, h = element.GetSize(canvas)
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
                
        element.SetPosition(pos)
    
    def ResizeElement(self, element, canvas):
        '''
        Resizes element to match grid spacing.
        Each corner is moved outwards to nearest grid intersection.
        '''
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
        
        w, h = element.GetSize(canvas)
        minw, minh = element.GetMinimalSize(canvas)
        dw = -(w % self.hor_spacing)
        dh = -(h % self.ver_spacing)
        if minw > w + dw:
            dw = self.hor_spacing + dw
        if minh > h + dh:
            dh = self.ver_spacing + dh
        rel = element.GetSizeRelative()
        element.SetSizeRelative((rel[0] + dw, rel[1] + dh))
        if self.snap_mode == 'CENTER':
            w, h = element.GetSize(canvas)
            dw = self.hor_spacing if w % (self.hor_spacing * 2) else 0
            dh = self.ver_spacing if h % (self.ver_spacing * 2) else 0
            if dw or dh:
                rel = element.GetSizeRelative()
                element.SetSizeRelative((rel[0] + dw, rel[1] + dh))
        
    def SnapConnection(self, conn, pos, idx, canvas, override=False):
        if not self.local_settings:
            self.hor_spacing = config['/Grid/HorSpacing']
            self.ver_spacing = config['/Grid/VerSpacing']
            self.snap_breakpoints = config['/Grid/SnapBreakpoints'] == 'true'
            self.active = config['/Grid/Active'] == 'true'
        if (self.active and self.snap_breakpoints) or override:
            pos = self.SnapPosition(pos)
        conn.MovePoint(canvas, pos, idx)
    
    def IsActive(self):
        if not self.local_settings:
            self.active = config['/Grid/Active'] == 'true'
        return self.active
        
    def IsVisible(self):
        if not self.local_settings:
            self.visible = config['/Grid/Visible'] == 'true'
        return self.visible
    
