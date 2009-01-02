from lib.config import config
from lib.Drawing.Context import CParamEval

class CConnectionLine(object):
    """
    Line that visualy represents the connection
    """
    def __init__(self, color = 'black', style = 'solid', width = 1):
        """
        Initialize line and set its style
        
        @param color: Color of the line (in HTML format)
        @type  color: string
        
        @param style: line style
        @type  style: string
        
        @param width: width of the line
        @type  width: integer or string
        """
        self.color = color
        self.style = style
        self.width = int(width)
    
    def ParseVariables(self, context, *vals):
        for val in vals:
            if not isinstance(val, (str, unicode)):
                yield val
            elif val[0] == '#':
                if val[1] == '#':
                    yield val[1:]
                else:
                    yield CParamEval(val[1:])(context)
            else:
                yield val
    
    def GetVariables(self, context, *names):
        return self.ParseVariables(context, *(getattr(self, name) for name in names))

    def Paint(self, context, start, end):
        """
        Paint the line on given canvas
        
        @param context: context in which is line being drawn
        @type  context: L{CAbstractCanvas<lib.Drawing.Context.DrawingContext.CDrawingContext>}
        
        @param start: starting coordinates of the line
        @type  start: (int, int)
        
        @param end: ending coordinates of the line
        @type  end: (int, int)
        """
        color, = self.GetVariables(context, 'color')
        context.GetCanvas().DrawLine(start, end, color, line_width = self.width, line_style = self.style)
