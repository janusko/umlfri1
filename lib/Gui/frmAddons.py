from lib.Depend.gtk2 import gtk, glib, pango

from lib.Drawing.Canvas.GtkPlus import PixmapFromPath

from common import event, CWindow

class CfrmAddons(CWindow):
    widgets = (
        'twMetamodelList', 'cmdInstallMetamodel', 'cmdUninstallMetamodel', 'cmdEnableMetamodel', 'cmdDisableMetamodel'
    )
    
    name = 'frmAddons'
    
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
            enabled = True
            uri = addon.GetUri()
            
            twStore.append(None, (icon, "<b>%s</b>     %s\n%s"%(
                glib.markup_escape_text(name),
                glib.markup_escape_text(version),
                glib.markup_escape_text(description)
            ), enabled, uri))
