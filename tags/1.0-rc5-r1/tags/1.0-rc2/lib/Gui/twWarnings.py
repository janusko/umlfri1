from lib.Depend.gtk2 import gobject
from lib.Depend.gtk2 import gtk

from lib.Gui.common import CWidget, event

ID_ICON, ID_DATETIME, ID_NAME, ID_TEXT, ID_PARAMS = range(5)

class CtwWarnings(CWidget):
    name = 'twWarnings'
    widgets = ('twWarnings', 'scrollWarnings')
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
        
        self.__treeStore = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
        
        self.scrollWarnings.hide()
        
        self.twWarnings.set_model(self.__treeStore)
        
        renderer = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('')
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'stock-id', ID_ICON)
        self.twWarnings.append_column(column)
        
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Date/Time'))
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', ID_DATETIME)
        self.twWarnings.append_column(column)
        
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Error name'))
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', ID_NAME)
        self.twWarnings.append_column(column)
        
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Error text'))
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', ID_TEXT)
        self.twWarnings.append_column(column)
    
    @event("twWarnings", "row-activated")
    def OntwWarningsRowActivate(self, treeView, path, column):
        iter = self.__treeStore.get_iter(path)
        params, = self.__treeStore.get(iter, ID_PARAMS)
        
        self.application.GetWindow('frmWarning').SetWarningInfo(*params)
        self.application.GetWindow('frmWarning').Show()
    
    def __refresh(self):
        self.__treeStore.clear()
        
        for item in self.application.warnings:
            self.__addWarning(item)
    
    def __addWarning(self, item):
        date, warning, category, file, lineno, line = item
        self.__treeStore.append(None, (gtk.STOCK_DIALOG_WARNING, date.strftime('%d.%m.%Y %H:%M'), category.__name__, str(warning), item))
    
    def Show(self):
        self.__refresh()
        self.application.warnings.connect(self.__addWarning)
        
        self.scrollWarnings.show()
    
    def Hide(self):
        self.scrollWarnings.hide()
        
        self.application.warnings.disconnect(self.__addWarning)
        self.__treeStore.clear()
