from lib.Depend.gtk2 import gtk

import common
from lib.consts import ADDON_EXTENSION, PROJECT_EXTENSION

class CfrmSelectAddon(common.CWindow):
    name = 'frmSelectAddon'
    glade = 'addons.glade'
    
    def __init__(self, app, wTree):
        common.CWindow.__init__(self, app, wTree)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Addon"))
        filter.add_pattern('*'+ADDON_EXTENSION)
        self.form.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Project with embedded metamodels"))
        filter.add_pattern('*'+PROJECT_EXTENSION)
        self.form.add_filter(filter)
    
    def ShowDialog(self, parent):
        self.form.set_transient_for(parent.form)
        try:
            while True:
                if self.form.run() == gtk.RESPONSE_CANCEL:
                    self.form.hide()
                    return None, None
                
                if self.form.get_filter() is None:
                    continue
                
                filter = self.form.get_filter().get_name()
                
                if filter == _("UML .FRI Project with embedded metamodels"):
                    type = 'projectMetamodel'
                else:
                    type = 'addon'
                
                return self.form.get_filename(), type
        finally:
            self.form.hide()
