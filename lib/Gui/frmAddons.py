from lib.Depend.gtk2 import gtk, pango, glib

import os.path
import webbrowser

import lib.consts
from lib.Drawing.Canvas.GtkPlus import PixmapFromPath

from common import event, CWindow
from dialogs import CQuestionDialog
import time

class PluginStartStop(object):
    def __init__(self, application, addon, startStop):
        self.__application = application
        self.__addon = addon
        self.__status = startStop
        self.__time = time.time()
    
    def GetStatus(self):
        return self.__status
    
    def Step(self):
        if self.__status == 'start':
            if self.__addon.IsRunning():
                self.__addon.Enable()
                self.__status = 'done'
        else:
            if not self.__addon.IsRunning():
                self.__addon.Disable()
                self.__status = 'done'
            elif time.time() - self.__time > lib.consts.PLUGIN_KILL_SECONDS:
                self.__time = time.time()
                
                if self.__application.GetWindow('frmAddons').IsVisible():
                    parent = self.__application.GetWindow('frmAddons')
                else:
                    parent = self.__application.GetWindow('frmMain')
                killDialog = self.__application.GetWindow('frmTerminateAddon')
                kill = killDialog.ShowDialog(parent, self.__addon)
                
                if kill:
                    if self.__status == 'stop':
                        self.__status = 'terminate'
                        self.__addon.Terminate()
                    else:
                        self.__status = 'error'
                        self.__addon.Kill()

class CfrmAddons(CWindow):
    name = 'frmAddons'
    glade = 'addons.glade'
    
    widgets = (
        'twMetamodelList', 'cmdInstallMetamodel', 'cmdUninstallMetamodel', 'cmdEnableMetamodel', 'cmdDisableMetamodel',
        'mnuMetamodel', 'mnuUninstallMetamodel', 'mnuEnableMetamodel', 'mnuDisableMetamodel',
        'mnuHomepageMetamodel', 'mnuAboutMetamodel',
        
        'twPluginList', 'cmdInstallPlugin', 'cmdUninstallPlugin', 'cmdPluginPreferences', 'cmdPluginStart', 'cmdPluginStop',
        'mnuPlugin', 'mnuUninstallPlugin', 'mnuStartPlugin', 'mnuStopPlugin',
        'mnuHomepagePlugin', 'mnuAboutPlugin',
    )
    
    COLUMN_ICON, COLUMN_DESCRIPTION, COLUMN_ENABLED, COLUMN_URI = range(4)
    
    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        
        self.__MetamodelStore = self.__InitTw(self.twMetamodelList)
        self.__PluginStore = self.__InitTw(self.twPluginList)
        self.__StartStopTimerId = None
        self.__ToStartStop = []
        
    def __InitTw(self, tw):
        store = gtk.TreeStore(gtk.gdk.Pixbuf, str, bool, str)
        tw.set_model(store)
        
        renderer = gtk.CellRendererPixbuf()
        renderer.set_property('yalign', 0)
        renderer.set_property('ypad', 3)
        column = gtk.TreeViewColumn()
        column.pack_start(renderer)
        column.add_attribute(renderer, 'pixbuf', 0)
        column.add_attribute(renderer, 'sensitive', 2)
        tw.append_column(column)
        
        renderer = gtk.CellRendererText()
        renderer.set_property('wrap-mode', pango.WRAP_WORD)
        column = gtk.TreeViewColumn()
        column.pack_start(renderer)
        column.add_attribute(renderer, 'markup', 1)
        column.add_attribute(renderer, 'sensitive', 2)
        tw.append_column(column)
        tw.connect_after("size-allocate", self.__DoTextWrap, column, renderer)
        
        return store

    def Show(self):
        self.__Load()
        glib.timeout_add(250, self.__ReLoadTimer)
        
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
        self.__PluginStore.clear()
        
        for addon in self.application.GetAddonManager().ListAddons():
            if addon.GetType() == 'metamodel':
                twStore = self.__MetamodelStore
            elif addon.GetType() == 'plugin':
                twStore = self.__PluginStore
            elif addon.GetType() == 'composite':
                twStore = self.__PluginStore
            else:
                continue
            
            iter = twStore.append(None)
            self.__SetAddonValues(twStore, iter, addon)
    
    def __SetAddonValues(self, store, iter, addon):
        if addon.GetIcon() is None:
            icon = None
        else:
            try:
                icon = PixmapFromPath(addon.GetStorage(), addon.GetIcon())
            except:
                icon = None
        
        name = addon.GetName()
        version = addon.GetVersion()
        description = addon.GetDescription() or ""
        enabled = self.__AddonEnabled(addon)
        uri = addon.GetDefaultUri()
        
        store.set(iter,
            self.COLUMN_ICON, icon,
            self.COLUMN_DESCRIPTION, "<b>%s</b>     %s\n%s"%(name, version, description),
            self.COLUMN_ENABLED, enabled,
            self.COLUMN_URI, uri
        )
    
    def __AddonEnabled(self, addon):
        if addon.GetType() == 'metamodel':
            return addon.IsEnabled()
        else:
            return addon.IsRunning()
    
    def __ReLoad(self):
        for model in (self.__MetamodelStore, self.__PluginStore):
            iter = model.get_iter_first()
            
            while iter is not None:
                uri, enabled = model.get(iter, self.COLUMN_URI, self.COLUMN_ENABLED)
                addon = self.application.GetAddonManager().GetAddon(uri)
                
                if enabled != self.__AddonEnabled(addon):
                    model.set(iter, self.COLUMN_ENABLED, not enabled)
                    
                    if addon == self.__GetSelectedAddon(self.twMetamodelList):
                        self.MetamodelChanged()
                    elif addon == self.__GetSelectedAddon(self.twPluginList):
                        self.PluginChanged()
                
                iter = model.iter_next(iter)
    
    def __ReLoadTimer(self):
        if not self.form.get_property("visible"):
            return False
        
        self.__ReLoad()
        
        return True
    
    def __GetSelectedAddon(self, treeView, path = None):
        if path is not None:
            iter = treeView.get_model().get_iter(path)
        else:
            iter = treeView.get_selection().get_selected()[1]
        
        if iter is None:
            return None
        
        selected = treeView.get_model().get(iter, 3)[0]
        return self.application.GetAddonManager().GetAddon(selected)
    
    def __StartStopTimer(self):
        for addon in self.__ToStartStop[:]:
            addon.Step()
            
            if addon.GetStatus() == 'done':
                self.__ToStartStop.remove(addon)
        
        if self.__ToStartStop:
            return True
        else:
            self.__StartStopTimerId = None
            return False
    
    @event("cmdEnableMetamodel", "clicked")
    @event("mnuEnableMetamodel", "activate")
    def on_cmdEnableMetamodel_click(self, button):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        if addon is None:
            return
        
        addon.Enable()
    
    @event("cmdDisableMetamodel", "clicked")
    @event("mnuDisableMetamodel", "activate")
    def on_cmdDisableMetamodel_click(self, button):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        
        if addon is None:
            return
        
        addon.Disable()
    
    @event("cmdInstallPlugin", "clicked")
    @event("cmdInstallMetamodel", "clicked")
    def on_InstallAddon(self, button):
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
            
            addon = self.application.GetAddonManager().LoadAddon(addonFile)
        
        if addon is None:
            return
        
        if self.application.GetWindow("frmInstallAddon").ShowDialog(self, addon):
            self.application.GetAddonManager().InstallAddon(addon)
            self.__Load()
    
    @event("cmdUninstallMetamodel", "clicked", "twMetamodelList")
    @event("mnuUninstallMetamodel", "activate", "twMetamodelList")
    def on_UninstallAddon(self, button, tw):
        addon = self.__GetSelectedAddon(getattr(self, tw))
        
        if addon is None:
            return
        
        if CQuestionDialog(self.form, _("Do you really want to uninstall addon '%(name)s %(version)s'?\nThis is pernament.")%{'name': addon.GetName(), 'version': addon.GetVersion()}).run():
            addon.Uninstall()
            self.__Load()
    
    @event("mnuHomepageMetamodel", "activate")
    def on_mnuHomepageMetamodel_click(self, button):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        
        if addon is None:
            return
        
        webbrowser.open_new_tab(addon.GetHomepage())
    
    @event("mnuAboutMetamodel", "activate")
    def on_mnuAboutMetamodel_click(self, button):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        
        if addon is None:
            return
        
        self.application.GetWindow("frmAboutAddon").ShowDialog(self, addon)
    
    @event("twMetamodelList", "cursor-changed")
    def MetamodelChanged(self, treeView = None):
        addon = self.__GetSelectedAddon(self.twMetamodelList)
        
        if addon is None:
            self.cmdEnableMetamodel.set_sensitive(False)
            self.cmdDisableMetamodel.set_sensitive(False)
            self.cmdUninstallMetamodel.set_sensitive(False)
        else:
            enabled = self.__AddonEnabled(addon)
            self.cmdEnableMetamodel.set_sensitive(not enabled)
            self.cmdDisableMetamodel.set_sensitive(enabled)
            self.cmdUninstallMetamodel.set_sensitive(addon.IsUninstallable())
    
    @event("twMetamodelList", "button-press-event")
    def MetamodelPopup(self, treeView, event):
        if event.button == 3:
            path = self.twMetamodelList.get_path_at_pos(event.x, event.y)
            if path is None:
                return
            addon = self.__GetSelectedAddon(self.twMetamodelList, path[0])
            if addon is not None:
                enabled = self.__AddonEnabled(addon)
                self.mnuEnableMetamodel.set_sensitive(not enabled)
                self.mnuDisableMetamodel.set_sensitive(enabled)
                self.mnuUninstallMetamodel.set_sensitive(addon.IsUninstallable())
                self.mnuHomepageMetamodel.set_sensitive(addon.GetHomepage() is not None)
                
                self.mnuMetamodel.popup(None, None, None, event.button, event.time)
    
    @event("mnuHomepagePlugin", "activate")
    def on_mnuHomepagePlugin_click(self, button):
        addon = self.__GetSelectedAddon(self.twPluginList)
        
        if addon is None:
            return
        
        webbrowser.open_new_tab(addon.GetHomepage())
    
    @event("mnuAboutPlugin", "activate")
    def on_mnuAboutPlugin_click(self, button):
        addon = self.__GetSelectedAddon(self.twPluginList)
        
        if addon is None:
            return
        
        self.application.GetWindow("frmAboutAddon").ShowDialog(self, addon)
    
    @event("twPluginList", "cursor-changed")
    def PluginChanged(self, treeView = None):
        addon = self.__GetSelectedAddon(self.twPluginList)
        
        if addon is None:
            self.cmdPluginStart.set_sensitive(False)
            self.cmdPluginStop.set_sensitive(False)
            self.cmdUninstallPlugin.set_sensitive(False)
        else:
            enabled = self.__AddonEnabled(addon)
            self.cmdPluginStart.set_sensitive(not enabled)
            self.cmdPluginStop.set_sensitive(enabled)
            self.cmdUninstallPlugin.set_sensitive(addon.IsUninstallable())
    
    @event("twPluginList", "button-press-event")
    def PluginPopup(self, treeView, event):
        if event.button == 3:
            path = self.twPluginList.get_path_at_pos(event.x, event.y)
            if path is None:
                return
            addon = self.__GetSelectedAddon(self.twPluginList, path[0])
            if addon is not None:
                enabled = self.__AddonEnabled(addon)
                self.mnuStartPlugin.set_sensitive(not enabled)
                self.mnuStopPlugin.set_sensitive(enabled)
                self.mnuUninstallPlugin.set_sensitive(addon.IsUninstallable())
                self.mnuHomepagePlugin.set_sensitive(addon.GetHomepage() is not None)
                
                self.mnuPlugin.popup(None, None, None, event.button, event.time)
    
    @event("mnuStartPlugin", "activate")
    @event("cmdPluginStart", "clicked")
    def on_cmdPluginStart_click(self, button):
        addon = self.__GetSelectedAddon(self.twPluginList)
        
        if addon is not None and not addon.IsRunning():
            addon.Start()
            self.__ToStartStop.append(PluginStartStop(self.application, addon, 'start'))
            if self.__StartStopTimerId is None:
                self.__StartStopTimerId = glib.timeout_add(100, self.__StartStopTimer)
    
    @event("mnuStopPlugin", "activate")
    @event("cmdPluginStop", "clicked")
    def on_cmdPluginStop_click(self, button):
        addon = self.__GetSelectedAddon(self.twPluginList)
        
        if addon is not None and addon.IsRunning():
            addon.Stop()
            self.__ToStartStop.append(PluginStartStop(self.application, addon, 'stop'))
            if self.__StartStopTimerId is None:
                self.__StartStopTimerId = glib.timeout_add(100, self.__StartStopTimer)
