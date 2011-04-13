from lib.Depend.gtk2 import gtk

import common

from lib.consts import PROJECT_EXTENSION, PROJECT_CLEARXML_EXTENSION, PROJECT_TPL_EXTENSION

from win32 import COpenSaveDialog

import os.path

class CfrmSave(common.CWindow):
    name = 'frmSave'
    glade = 'project.glade'
    
    def __init__(self, app, wTree):
        common.CWindow.__init__(self, app, wTree)

        self.filters = [
            (_("UML .FRI Projects"), "*"+PROJECT_EXTENSION, True),
            (_("UML .FRI Clear XML Projects"), "*"+PROJECT_CLEARXML_EXTENSION, False),
            (_("UML .FRI Projects templates"), "*"+PROJECT_TPL_EXTENSION, True),
        ]
        
        for text, pattern, zipped in self.filters:
            filter = gtk.FileFilter ()
            filter.set_name (text)
            filter.add_pattern (pattern)
            self.form.add_filter (filter)
    
    def ShowDialog(self, parent):
        if COpenSaveDialog:
            win = COpenSaveDialog(parent.form, 'save', self.form.get_title(), self.filters)
            if win.ShowModal():
                filename = win.GetAbsolutePath()
                filter = win.GetSelectedFilter()
                
                if '.' not in os.path.basename(filename):
                    filename += filter[1][1:]
                
                return filename, filter[2]
            else:
                return None, None
        
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
                
                ext = ''
                isZippedFile = False
                
                for text, pattern, zipped in self.filters:
                    if text == filter:
                        ext = pattern[1:]
                        isZippedFile = zipped
                
                if '.' not in os.path.basename(filename):
                    filename += ext
                
                if not os.path.isdir(filename):
                    self.application.GetRecentFiles().AddFile(filename)
                    return filename, isZippedFile
                
        finally:
            self.form.hide()
