from VisualObject import CVisualObject
from ..IconSizeMeasurer import GetIconSize
# import sys

class CIcon(CVisualObject):
    types = {
        'filename': str
    }
    def __init__(self, filename):
        CVisualObject.__init__(self)
        self.filename = filename

    def ComputeSize(self, context):
        filename, = self.GetVariables(context, 'filename')
        return GetIconSize(context.GetMetamodel().GetStorage(), filename)

    def Paint(self, context, canvas):
        filename, = self.GetVariables(context, 'filename')
        
        canvas.DrawIcon(context.GetPos(), filename)
