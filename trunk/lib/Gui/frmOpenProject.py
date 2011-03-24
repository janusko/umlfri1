from lib.Depend.gtk2 import gtk

import common

from lib.consts import PROJECT_EXTENSION, PROJECT_CLEARXML_EXTENSION, PROJECT_TPL_EXTENSION

import os.path

class CfrmOpenProject (common.CWindow):
    name = "frmOpenProject"

    glade = "project.glade"

    widgets = ("chkOpenAsCopy", )

    def __init__ (self, app, wTree):
        common.CWindow.__init__ (self, app, wTree)

        filter = gtk.FileFilter ()
        filter.set_name (_("UML .FRI Projects"))
        filter.add_pattern ("*"+PROJECT_EXTENSION)
        self.form.add_filter (filter)

        filter = gtk.FileFilter ()
        filter.set_name (_("UML .FRI Clear XML Projects"))
        filter.add_pattern ("*"+PROJECT_CLEARXML_EXTENSION)
        self.form.add_filter (filter)

        filter = gtk.FileFilter ()
        filter.set_name (_("UML .FRI Projects templates"))
        filter.add_pattern ("*"+PROJECT_TPL_EXTENSION)
        self.form.add_filter (filter)

        filter = gtk.FileFilter ()
        filter.set_name (_("All files"))
        filter.add_pattern ("*")
        self.form.add_filter (filter)

    def ShowDialog (self, parent):
        self.form.set_transient_for (parent.form)
        self.chkOpenAsCopy.set_active (False)
        try:
            while True:
                run  = self.form.run ()
                print run
                if run != gtk.RESPONSE_OK:
                    self.form.hide ()
                    return None, None
                copy = self.chkOpenAsCopy.get_active ()
                filename = self.form.get_filename ()
                if not filename:
                    continue
                else:
                    filename = filename.decode ('utf-8')
                if filename and os.path.isfile (filename):
                    if not copy:
                        self.application.GetRecentFiles ().AddFile (filename)
                    return filename, copy
        finally:
            self.form.hide ()