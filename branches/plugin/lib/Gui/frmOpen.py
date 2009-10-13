from lib.Depend.gtk2 import gtk

import common
import lib.consts
from lib.config import config
import os
import os.path
import gobject
import zipfile
from dialogs import CWarningDialog
from common import event
import sys

class CfrmOpen(common.CWindow):
    name = 'frmOpen'
    glade = 'project.glade'
    
    widgets = ("ivOpenNew", "fwOpenExisting", "chkOpenAsCopyExisting", "twOpenRecent", "chkOpenAsCopyRecent", "nbOpen")
    
    def __init__(self, app, wTree):
        common.CWindow.__init__(self, app, wTree)
        
        self.ivOpenModel = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf, gobject.TYPE_PYOBJECT)
        self.ivOpenNew.set_model(self.ivOpenModel)
        self.ivOpenNew.set_text_column(0)
        self.ivOpenNew.set_pixbuf_column(1)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Projects"))
        filter.add_pattern('*'+lib.consts.PROJECT_EXTENSION)
        self.fwOpenExisting.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Clear XML Projects"))
        filter.add_pattern('*'+lib.consts.PROJECT_CLEARXML_EXTENSION)
        self.fwOpenExisting.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(_("UML .FRI Project templates"))
        filter.add_pattern('*'+lib.consts.PROJECT_TPL_EXTENSION)
        self.fwOpenExisting.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        self.fwOpenExisting.add_filter(filter)
        
        self.listStore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        self.twOpenRecent.set_model(self.listStore)
        self.twOpenRecent.append_column(gtk.TreeViewColumn('', gtk.CellRendererPixbuf(), pixbuf = 2))
        self.twOpenRecent.append_column(gtk.TreeViewColumn(_('File name'), gtk.CellRendererText(), text = 0))
        self.twOpenRecent.append_column(gtk.TreeViewColumn(_('Date'), gtk.CellRendererText(), text = 1))
    
    def __GetIcon(self, filename):
        if not os.path.isfile(filename):
            return gtk.gdk.pixbuf_new_from_file(config['/Paths/Images']+lib.consts.DEFAULT_TEMPLATE_ICON)
        f = os.tempnam()
        ext = filename.split('.')
        ext.reverse()
        
        if (("."+ext[0]) != lib.consts.PROJECT_CLEARXML_EXTENSION):
            try:
                z = zipfile.ZipFile(filename)
                for i in z.namelist():
                    if i in ('icon.png', 'icon.gif', 'icon.jpg', 'icon.ico', 'icon.png'):
                        file(f, 'wb').write(z.read(i))
                        ret = gtk.gdk.pixbuf_new_from_file(f)
                        os.unlink(f)
                        return ret
            except zipfile.BadZipfile:
                pass

        return gtk.gdk.pixbuf_new_from_file(config['/Paths/Images']+lib.consts.DEFAULT_TEMPLATE_ICON)
    
    def __ReloadOpenRecentList(self):
        self.listStore.clear()
        for name, date in self.application.GetRecentFiles().GetRecentFiles():
            iter = self.listStore.append()
            self.listStore.set(iter,0,name.encode('utf-8'),1,date, 2, self.__GetIcon(name))
    
    @event("fwOpenExisting", "file-activated")
    def on_fwOpenExisting_file_activated(self, widget):
        self.form.response(gtk.RESPONSE_OK)
    
    @event("ivOpenNew", "item-activated")
    def on_ivOpenNew_item_activated(self, widget, path):
        self.form.response(gtk.RESPONSE_OK)
    
    @event("twOpenRecent", "row-activated")
    def on_twOpenRecent_doubleclick(self, treeView, path, column):
        self.form.response(gtk.RESPONSE_OK)
        
    
    def ShowDialog(self, parent, tab = 0):
        self.nbOpen.set_current_page(tab)
        self.fwOpenExisting.set_current_folder_uri(self.fwOpenExisting.get_current_folder_uri())
        
        self.ivOpenModel.clear()
        templates = []
        for dirname in (config['/Paths/Templates'], config['/Paths/UserTemplates']):
            if os.path.exists(dirname):
                templates.extend((dirname, filename) for filename in os.listdir(dirname))
        for dirname, filename in templates:
            if filename.endswith(lib.consts.PROJECT_TPL_EXTENSION):
                iter = self.ivOpenModel.append()
                self.ivOpenModel.set(iter, 0, filename[:-len(lib.consts.PROJECT_TPL_EXTENSION)],
                                           1, self.__GetIcon(os.path.join(dirname, filename)),
                                           2, os.path.join(dirname, filename))
        
        self.__ReloadOpenRecentList()
        self.form.set_transient_for(parent.form)
        self.chkOpenAsCopyExisting.set_active(False)
        self.chkOpenAsCopyRecent.set_active(False)
        try:
            while True:
                if self.form.run() != gtk.RESPONSE_OK:
                    self.form.hide()
                    return None, False
                if self.nbOpen.get_current_page() == 0:
                    tmp = self.ivOpenNew.get_selected_items()
                    if tmp: 
                        iter = self.ivOpenModel.get_iter(tmp[0])
                        return self.ivOpenModel.get(iter, 2)[0], True # template
                elif self.nbOpen.get_current_page() == 1:
                    copy = self.chkOpenAsCopyExisting.get_active()
                    filename = self.fwOpenExisting.get_filename()
                    if filename is None:
                        continue
                    else:
                        filename = filename.decode('utf-8')
                    if filename is not None and os.path.isfile(filename):
                        if not copy:
                            self.application.GetRecentFiles().AddFile(filename)
                        return filename, copy # existing
                else:
                    copy = self.chkOpenAsCopyRecent.get_active()
                    iter = self.twOpenRecent.get_selection().get_selected()[1]
                    if iter is not None:
                        filename = self.twOpenRecent.get_model().get(iter,0)[0].decode('utf-8')
                        if not copy:
                            self.application.GetRecentFiles().AddFile(filename)
                        if not os.path.exists(filename):  
                            self.application.GetRecentFiles().RemoveFile(filename)
                            CWarningDialog(self.form, _("File does not exist")).run()
                            self.__ReloadOpenRecentList()
                        else:
                            return filename, copy # recent
        finally:
            self.form.hide()