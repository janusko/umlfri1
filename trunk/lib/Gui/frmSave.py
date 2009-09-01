from lib.Depend.gtk2 import gtk

import common

from lib.consts import PROJECT_EXTENSION, PROJECT_CLEARXML_EXTENSION, PROJECT_TPL_EXTENSION

import os.path

class CfrmSave(common.CWindow):
    name = 'frmSave'
    glade = 'project.glade'
    
    def __init__(self, app, wTree):
        common.CWindow.__init__(self, app, wTree)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Projects"))
        filter.add_pattern('*'+PROJECT_EXTENSION)
        self.form.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Clear XML Projects"))
        filter.add_pattern('*'+PROJECT_CLEARXML_EXTENSION)
        self.form.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Project templates"))
        filter.add_pattern('*'+PROJECT_TPL_EXTENSION)
        self.form.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        self.form.add_filter(filter)

        self.zippedFileExtensions = [_("UML .FRI Projects"), _("UML .FRI Project templates")]
    
    def ShowDialog(self, parent):
        self.form.set_transient_for(parent.form)
        try:
            while True:
                if self.form.run() == gtk.RESPONSE_CANCEL:
                    self.form.hide()
                    return None, None
                filter = self.form.get_filter().get_name()
                filename = self.form.get_filename()
                if filename is None:
                    self.form.hide()
                    return None, None
                else:
                    filename = filename.decode('utf-8')
                if '.' not in os.path.basename(filename):
                    if filter == _("UML .FRI Projects"):
                        filename += PROJECT_EXTENSION
                        #isZippedFile = True
                    elif filter == _("UML .FRI Clear XML Projects"):
                        filename += PROJECT_CLEARXML_EXTENSION
                        #isZippedFile = False
                    elif filter == _("UML .FRI Project templates"):
                        filename += PROJECT_TPL_EXTENSION
                        #isZippedFile = True
                isZippedFile = filter in self.zippedFileExtensions
                if not os.path.isdir(filename):
                    self.application.GetRecentFiles().AddFile(filename)
                    return filename, isZippedFile
                
        finally:
            self.form.hide()
