from lib.Depend.gtk2 import cairo
from CairoBase import CCairoBaseCanvas

# basicaly just the CCairoBaseCanvas - defined for convienience and/or later possibility 
# to adapt the canvas for printing, if needed

class CPrintCanvas(CCairoBaseCanvas):
    def __init__(self, printingContext, storage = None):
        CCairoBaseCanvas.__init__(self, printingContext, storage)

           