from VisualObject import CVisualObject
from ..IconSizeMeasurer import GetIconSize
# import sys
from lib.lib import ParseScale


class CIcon(CVisualObject):
    types = {
        'filename': str,
        'scale': str
    }
    def __init__(self, filename, scale="1"):
        CVisualObject.__init__(self)
        self.filename = filename
        self.scale = scale

    def ComputeSize(self, context):
        filename, scale = self.__GetParameters(context)
        w, h = GetIconSize(context.GetMetamodel().GetStorage(), filename)
        return w * scale, h * scale

    def Paint(self, context, canvas):
        filename, scale = self.__GetParameters(context)
        
        canvas.DrawIcon(context.GetPos(), filename, scale)

    def __GetParameters(self, context):
        filename, scale = self.GetVariables(context, 'filename', 'scale')
        scale = ParseScale(scale)
        return filename, scale