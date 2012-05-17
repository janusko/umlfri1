from lib.Depend.gtk2 import gtk

import common
from lib.GenericGui import CFileType

from win32 import COpenSaveDialog

import os.path

import thread

import gobject

class CfrmFileImportExportBase(common.CWindow):
    glade = 'project.glade'

    def __init__(self, app, wTree, type):
        common.CWindow.__init__(self, app, wTree)
        
        self.__type = type

    def OnOk(self, filename, fileType):
        pass

    def __NewDialog(self, parent, title, fileTypes):
        filters = [(fileType.GetDescription(), ';'.join(fileType.GetExtensions())) for fileType in fileTypes]
        
        win = COpenSaveDialog(parent.form, 'save' if self.__type == 'export' else 'open', title, filters)
        if win.ShowModal():
            filename = win.GetAbsolutePath()
            filterIndex = win.GetSelectedFilterIndex()
            gobject.idle_add(self.OnOk, filename, fileTypes[filterIndex])
    
    def ShowDialog(self, parent):
        if self.__type == 'export':
            isPossible = CFileType.GetExportPossible
        else:
            isPossible = CFileType.GetImportPossible
        
        fileTypes = [fileType for fileType in self.application.GetFileTypeManager().GetFileTypes() if isPossible(fileType)]
        
        if COpenSaveDialog:
            thread.start_new(self.__NewDialog, (parent, self.form.get_title(), fileTypes))
        else:
            for fileType in fileTypes:
                filter = gtk.FileFilter()
                filter.set_name(fileType.GetDescription())
                for extension in fileType.GetExtensions():
                    filter.add_pattern('*.' + extension)
                self.form.add_filter(filter)
            
            self.form.set_transient_for(parent.form)
            try:
                while True:
                    if self.form.run() == gtk.RESPONSE_CANCEL:
                        self.form.hide()
                        return
                    filename = self.form.get_filename()
                    if filename is None:
                        self.form.hide()
                        return
                    
                    filename = filename.decode('utf-8')
                    if not os.path.isdir(filename):
                        self.form.hide()
                        filterIndex = self.form.list_filters().index(self.form.get_filter())
                        self.OnOk(filename, fileTypes[filterIndex])
                        return

            finally:
                self.form.hide()
