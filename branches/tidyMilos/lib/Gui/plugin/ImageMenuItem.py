import lib.GenericGui
from lib.Depend.gtk2 import gtk
from MenuItem import CMenuItem

class CImageMenuItem(lib.GenericGui.CImageMenuItem, CMenuItem):
    
    def _setImage(self, filename):
        if filename:
            image = gtk.Image()
            image.set_from_file(filename)
        else:
            image = None
        self.obj.set_image(image)
    
    def SetImageFromFile(self, filename):
        self._setImage(filename)
