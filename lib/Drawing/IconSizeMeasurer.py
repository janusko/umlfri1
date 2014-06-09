from Canvas.CairoBase import PixmapFromPath
from lib.Exceptions import DrawingError

def GetIconSize(storage, filename):
    if storage is None:
        raise DrawingError('storage')
    pixmap = PixmapFromPath(storage, filename)
    return pixmap.get_width(), pixmap.get_height() # + self.cr.scale(self.scale, self.scale)
