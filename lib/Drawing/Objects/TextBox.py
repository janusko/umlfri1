from VisualObject import CVisualObject
from ..TextSizeMeasurer import TextSizeMeasurer
import sys
from lib.datatypes import CColor, CFont

class CTextBox(CVisualObject):
    types = {
        'text': unicode,
        'color': CColor,
        'font': CFont
    }
    
    defaultColor = CColor("black")
    defaultFont = CFont("Arial 10")
    
    def __init__(self, text, color = None, font = None):
        CVisualObject.__init__(self)
        self.text = text
        self.color = color
        self.font = font
        self.textSizeMeasurer = TextSizeMeasurer()

    def ComputeSize(self, context):
        txt, font = self.GetVariables(context, 'text', 'font')
        txt = unicode(txt)
        
        if font is None:
            font = context.GetDefault('textfont')
            if font is None:
                font = self.defaultFont

        return self.textSizeMeasurer.MeasureSize(txt, font)

    def Paint(self, context, canvas):
        txt, color, font = self.GetVariables(context, 'text', 'color', 'font')
        txt = unicode(txt)
        shadowcolor = context.GetShadowColor()
        if shadowcolor is not None:
            color = shadowcolor
        elif color is None:
            color = context.GetDefault('textcolor')
            if color is None:
                color = self.defaultColor
        
        if font is None:
            font = context.GetDefault('textfont')
            if font is None:
                font = self.defaultFont

        canvas.DrawText(context.GetPos(), txt, font, color)
