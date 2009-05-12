from VisualObject import CVisualObject
import sys
from lib.datatypes import CColor, CFont

class CTextBox(CVisualObject):
    types = {
        'text': unicode,
        'color': CColor,
        'font': CFont
    }
    def __init__(self, text, color = CColor("black"), font = CFont("Arial 10")):
        CVisualObject.__init__(self)
        self.text = text
        self.color = color
        self.font = font

    def ComputeSize(self, context):
        txt, font = self.GetVariables(context, 'text', 'font')
        return context.GetCanvas().GetTextSize(txt, font)

    def Paint(self, context):
        txt, color, font = self.GetVariables(context, 'text', 'color', 'font')
        txt = unicode(txt)
        shadowcolor = context.GetShadowColor()
        if shadowcolor is not None:
            color = shadowcolor
        
        context.GetCanvas().DrawText(context.GetPos(), txt, font, color)
