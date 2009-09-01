from lib.Depend.gtk2 import gtk

import common

class CfrmSelectAddonSource(common.CWindow):
    name = 'frmSelectAddonSource'
    glade = 'addons.glade'
    
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
