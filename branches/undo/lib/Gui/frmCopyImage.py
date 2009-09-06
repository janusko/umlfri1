from lib.Depend.gtk2 import gtk

from common import CWindow, event
from lib.datatypes import CColor

class CfrmCopyImage(CWindow):
    name = 'frmCopyImage'
    glade = 'export.glade'
    
    widgets = ('spinCopyZoom','chkCopyTransparent', )
    
    def Show(self):
        try:
            if self.form.run() == gtk.RESPONSE_OK:
                zoom = self.spinCopyZoom.get_value_as_int()
                if self.chkCopyTransparent.get_active():
                    bg = None
                else:
                    bg = CColor("#FFFFFF")
                return zoom, bg
            else:
                return None, None
        finally:
            self.Hide()
