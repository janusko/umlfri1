from lib.Depend.gtk2 import gtk

import common
import lib.consts
import os.path
from lib.consts import ADDON_EXTENSION, PROJECT_EXTENSION

class CfrmSelectAddonSource(common.CWindow):
    name = 'frmSelectAddonSource'
    
    widgets = ('optInstallFromProject', 'optInstallFromFile')
    
    def ShowDialog(self, parent):
        self.optInstallFromProject.set_active(False)
        self.optInstallFromFile.set_active(True)
        
        self.form.set_transient_for(parent.form)
        
        try:
            while True:
                if self.form.run() != gtk.RESPONSE_OK:
                    return None
                
                print 'xxxx'
                
                if self.optInstallFromProject.get_active():
                    return 'project'
                else:
                    return 'file'
        finally:
            self.form.hide()
