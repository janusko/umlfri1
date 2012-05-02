from lib.Depend.gtk2 import gtk

import common

from lib.consts import PROJECT_EXTENSION, PROJECT_CLEARXML_EXTENSION, PROJECT_TPL_EXTENSION, PROJECT_TPL_CLEARXML_EXTENSION

from win32 import COpenSaveDialog

import os.path

import thread

import gobject

class CfrmImport (common.CWindow):
    name = "frmImport"

    glade = "project.glade"    

    def __init__ (self, app, wTree):
        common.CWindow.__init__ (self, app, wTree)

        self.filters = [
            (_("UML .FRI Projects"), "*"+PROJECT_EXTENSION),
            (_("UML .FRI Clear XML Projects"), "*"+PROJECT_CLEARXML_EXTENSION),
            (_("UML .FRI Projects templates"), "*"+PROJECT_TPL_EXTENSION),
            (_("UML .FRI Clear XML Project templates"), "*"+PROJECT_TPL_CLEARXML_EXTENSION),
        ]

        for text, pattern in self.filters:
            filter = gtk.FileFilter ()
            filter.set_name (text)
            filter.add_pattern (pattern)
            self.form.add_filter (filter)

    def __NewDialog(self, title, filters, parent, widget):
        win = COpenSaveDialog(parent.form, 'open', title, filters)
        if win.ShowModal():
            filename = win.GetAbsolutePath()
            filters = win.GetSelectedFilterIndex()
            win = filename, filters
        else:
            win =  None, None
        gobject.idle_add(parent.OnImport,(win))

    def ShowDialog (self, parent, widget):
        if COpenSaveDialog:
            title = self.form.get_title()
            filters = self.filters
            thread.start_new(self.__NewDialog,(title, filters, parent, widget))
            return None, None
        self.form.set_transient_for (parent.form)        
        try:
            while True:
                run  = self.form.run ()
                if run != gtk.RESPONSE_OK:
                    self.form.hide ()
                    parent.OnImport((None, None))
                    return                
                filename = self.form.get_filename ()                   
                if not filename:
                    continue
                else:
                    filename = filename.decode ('utf-8')
                if filename and os.path.isfile (filename):                    
                    filterIndex = self.form.list_filters().index(self.form.get_filter())
                    parent.OnImport((filename, filterIndex))
                    return
        finally:
            self.form.hide ()
