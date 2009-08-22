from lib.Depend.gtk2 import gtk, pango

import os.path

from lib.Drawing.Canvas.GtkPlus import PixmapFromPath

from common import event, CWindow
from dialogs import CQuestionDialog

class CfrmAddons(CWindow):
    name = 'frmAddons'
    glade = 'addons.glade'
    
    widgets = (
        'twMetamodelList', 'cmdInstallMetamodel', 'cmdUninstallMetamodel', 'cmdEnableMetamodel', 'cmdDisableMetamodel'
    )
    
    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        
        self.__MetamodelStore = gtk.TreeStore(gtk.gdk.Pixbuf, str, bool, str)
        self.twMetamodelList.set_model(self.__MetamodelStore)
        
        renderer = gtk.CellRendererPixbuf()
        renderer.set_property('yalign', 0)
        renderer.set_property('ypad', 3)
        column = gtk.TreeViewColumn()
        column.pack_start(renderer)
        column.add_attribute(renderer, 'pixbuf', 0)
        column.add_attribute(renderer, 'sensitive', 2)
        self.twMetamodelList.append_column(column)
        
        renderer = gtk.CellRendererText()
        renderer.set_property('wrap-mode', pango.WRAP_WORD)
        column = gtk.TreeViewColumn()
        column.pack_start(renderer)
        column.add_attribute(renderer, 'markup', 1)
        column.add_attribute(renderer, 'sensitive', 2)
        self.twMetamodelList.append_column(column)
        self.twMetamodelList.connect_after("size-allocate", self.__DoTextWrap, column, renderer)

    def Show(self):
        self.__Load()
        
        self.twMetamodelList.grab_focus()
        
        self.form.run()
        
        self.Hide()
    
    def __DoTextWrap(self, treeview, allocation, column, cell):
        otherColumns = (c for c in treeview.get_columns() if c != column)
        newWidth = allocation.width - sum(c.get_width() for c in otherColumns)
        newWidth -= treeview.style_get_property("horizontal-separator") * 2
        if cell.props.wrap_width == newWidth or newWidth <= 0:
            return
        cell.props.wrap_width = newWidth
        store = treeview.get_model()
        iter = store.get_iter_first()
        while iter and store.iter_is_valid(iter):
            store.row_changed(store.get_path(iter), iter)
            iter = store.iter_next(iter)
            treeview.set_size_request(0,-1)
    
    def __Load(self):
        self.__MetamodelStore.clear()
        
        for addon in self.application.addonManager.ListAddons():
            if addon.GetType() == 'metamodel':
                twStore = self.__MetamodelStore
            else:
                continue
            
            if addon.GetIcon() is None:
                icon = None
            else:
                icon = PixmapFromPath(addon.GetStorage(), addon.GetIcon())
            
            name = addon.GetName()
            version = addon.GetVersion()
            description = addon.GetDescription() or ""
            enabled = addon.IsEnabled()
            uri = addon.GetDefaultUri()
            
            twStore.append(None, (icon, "<b>%s</b>     %s\n%s"%(name, version, description), enabled, uri))
    
    def __GetSelectedAddon(self, treeView):
        iter = treeView.get_selection().get_selected()[1]
        if iter is None:
            return None
        
        selected = treeView.get_model().get(iter, 3)[0]
        return self.application.addonManager.GetAddon(selected)
    
    @event("cmdEnableMetamodel", "clicked")
    def on_cmdEnableMetamodel_click(self, button):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        if addon is None:
            return
        
        iter = self.twMetamodelList.get_selection().get_selected()[1]
        self.__MetamodelStore.set(iter, 2, True)
        
        addon.Enable()
        self.MetamodelChanged()
    
    @event("cmdDisableMetamodel", "clicked")
    def on_cmdDisableMetamodel_click(self, button):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        
        if addon is None:
            return
        
        iter = self.twMetamodelList.get_selection().get_selected()[1]
        self.__MetamodelStore.set(iter, 2, False)
        
        addon.Disable()
        self.MetamodelChanged()
    
    @event("cmdInstallMetamodel", "clicked")
    def on_cmdInstallMetamodel_click(self, button):
        addon = None
        
        if self.application.GetProject() is not None and self.application.GetProject().GetAddon() is not None:
            t = self.application.GetWindow("frmSelectAddonSource").ShowDialog(self)
            if t is None:
                return
            elif t == 'project':
                addon = self.application.GetProject().GetAddon()
        
        if addon is None:
            addonFile, type = self.application.GetWindow("frmSelectAddon").ShowDialog(self)
            
            if addonFile is None:
                return
            
            if type == 'projectMetamodel':
                addonFile = os.path.join(addonFile, 'metamodel')
            
            addon = self.application.addonManager.LoadAddon(addonFile)
        
        if addon is None:
            return
        
        if self.application.GetWindow("frmInstallAddon").ShowDialog(self, addon):
            self.application.addonManager.InstallAddon(addon)
            self.__Load()
    
    @event("cmdUninstallMetamodel", "clicked")
    def on_cmdUninstallMetamodel_click(self, button):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        
        if addon is None:
            return
        
        if CQuestionDialog(self.form, _("Do you really want to uninstall addon '%(name)s %(version)s'?\nThis is pernament.")%{'name': addon.GetName(), 'version': addon.GetVersion()}).run():
            addon.Uninstall()
            self.__Load()
    
    @event("twMetamodelList", "cursor-changed")
    def MetamodelChanged(self, treeView = None):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        
        if addon is None:
            self.cmdEnableMetamodel.set_sensitive(False)
            self.cmdDisableMetamodel.set_sensitive(False)
            self.cmdUninstallMetamodel.set_sensitive(False)
        else:
            self.cmdEnableMetamodel.set_sensitive(not addon.IsEnabled())
            self.cmdDisableMetamodel.set_sensitive(addon.IsEnabled())
            self.cmdUninstallMetamodel.set_sensitive(addon.IsUninstallable())
