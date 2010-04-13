from lib.Depend.gtk2 import gtk, gobject
from lib.Exceptions import *
import thread
from lib.Base import CBaseObject
from lib.Base.Registrar import registrar
import plugin

from warnings import warn

class CGuiManager(CBaseObject):
    '''
    Encapsulates handling of GUI modifications
    '''
    
    transformations = {
        gtk.MenuBar: plugin.CMenu,
        gtk.Menu: plugin.CMenu,
        gtk.Toolbar: plugin.CButtonBar,
        gtk.ToolButton: plugin.CButton,
        gtk.ToggleToolButton: plugin.CToggleButton,
        gtk.MenuItem: plugin.CMenuItem,
        gtk.ImageMenuItem: plugin.CImageMenuItem,
        gtk.CheckMenuItem: plugin.CCheckMenuItem,
        gtk.SeparatorMenuItem: plugin.CSeparator,
        gtk.SeparatorToolItem: plugin.CSeparator,
    }
    items = []
    
    def __init__(self, app):
        self.lock = thread.allocate()
        self.app = app
        self.frmMain = self.app.GetWindow('frmMain')
        self._persistent = True
        
    def GetItem(self, item):
        try:
            self.lock.acquire()
            if item is None:
                return None
            if hasattr(item, '_pluginShade'):
                return item._pluginShade
            else:
                cls = CGuiManager.transformations.get(item.__class__, None)
                if cls is None:
                    return None
                result = cls(item, self, item.get_name())
                item._pluginShade = result
                CGuiManager.items.append(result)
                return result
        finally:
            self.lock.release()
            
    
    def GetMainMenu(self):
        return self.GetItem(self.app.GetWindow('frmMain').mnuMenubar)
        
    def GetTabMenu(self):
        return self.GetItem(self.app.GetWindow('frmMain').nbTabs.mnuTab)
        
    def GetTreeMenu(self):
        return self.GetItem(self.app.GetWindow('frmMain').twProjectView.menuTreeElement)
    
    def GetDrawMenu(self):
        return self.GetItem(self.app.GetWindow('frmMain').picDrawingArea.pMenuShift)
    
    def GetButtonBar(self):
        return self.GetItem(self.app.GetWindow('frmMain').hndCommandBar.get_children()[0])
    
    def DisplayWarning(self, text):
        gobject.idle_add(self.app.GetBus().emit, 'run-dialog', 'warning', text)
    
