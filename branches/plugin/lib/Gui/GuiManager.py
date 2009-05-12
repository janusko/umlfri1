from lib.Depend.gtk2 import gtk
from lib.Exceptions import *
import thread

class CGuiManager(object):
    '''
    Encapsulates handling of GUI modifications
    '''
    
    def __init__(self, app):
        self.lock = thread.allocate()
        self.app = app
        frmMain = self.app.GetWindow('frmMain')
        self.menupaths = {
            'mnuMenubar': frmMain.mnuMenubar,
            'mnuMenubar/mItemFile': frmMain.mItemFile.get_submenu(),
            'mnuMenubar/mItemEdit': frmMain.mItemEdit.get_submenu(),
            'mnuMenubar/mItemProject': frmMain.mItemProject.get_submenu(),
            'mnuMenubar/mItemDiagram': frmMain.mItemDiagram.get_submenu(),
            'mnuMenubar/mItemElement': frmMain.mItemElement.get_submenu(),
            'mnuMenubar/mItemView': frmMain.mItemView.get_submenu(),
            'mnuMenubar/mItemHelp': frmMain.mItemHelp.get_submenu(),
            'mnuTab': frmMain.nbTabs.mnuTab,
            'mnuDrawing': frmMain.picDrawingArea.pMenuShift,
            'mnuTree': frmMain.twProjectView.menuTreeElement,
        }
        self.menuitems = {}
        self.buttonpaths = {
            'hndCommandBar': frmMain.hndCommandBar.get_children()[0],
        }
        self.buttonitems = {}
        self.belongs = {}
        
        
        
    def AddItem(self, mtype, path, name, callback, addr, **params):
        try:
            self.lock.acquire()
            if mtype in ('ImageMenuItem', 'MenuItem'):
                if mtype == 'ImageMenuItem':
                    if 'stock_id' in params:
                        item = gtk.ImageMenuItem(stock_id = params['stock_id'])
                    else:
                        item = gtk.ImageMenuItem(params['text'])
                        image = gtk.Image()
                        image.set_from_file(params['filename'])
                        item.set_image(image)
                else:
                    item = gtk.MenuItem(params['text'])
                item.connect('activate', callback, path + '/' + name, addr)
                item.show()
                self._AddMenuItem(item, name, path)
                return True
            
            elif mtype == 'ToolButton':
                if 'stock_id' in params:
                    item = gtk.ToolButton(params['stock_id'])
                else:
                    if 'filename' in params:
                        image = gtk.Image()
                        image.set_from_file(params['filename'])
                    else:
                        image = None
                    item = gtk.ToolButton(image, params['text'])
                item.connect('clicked', callback, path + '/' + name, addr)
                item.show()
                self._AddButton(item, name, path)
                return True
            elif mtype == 'submenu':
                self._AddSubmenu(path)
                return True
            
            else:
                raise ParamValueError('type')
        
        finally:
            self.lock.release()
        
        
    def SetSensitive(self, path, sensitive):
        try:
            self.lock.acquire()
            if path in self.menuitems:
                item = self.menuitems[path]
            elif path in self.buttonitems:
                item = self.buttonitems[path]
            else:
                raise ParamValueError('path')
            gtk.idle_add(item.set_property, 'sensitive', sensitive)
        finally:
            self.lock.release()
    
    def _AddMenuItem(self, item, name, path):
        self._AddItem(item, name, path, self.menupaths, self.menuitems)
    
    def _AddButton(self, button, name, path):
        self._AddItem(button, name, path, self.buttonpaths, self.buttonitems)
        
    def _AddSubmenu(self, path):
        if path not in self.menuitems or path in self.menupaths:
            raise ParamValueError('path')
        menu = gtk.Menu()
        gtk.idle_add(self.menuitems[path].set_submenu, menu)
        self.menupaths[path] = menu
            
    
    def _AddItem(self, item, name, path, paths, items):
        fullname = '/'.join((path, name))
        if path not in paths:
            raise ParamValueError('path')
        if fullname in items:
            raise ParamValueError('name')
        if path in paths and fullname not in items:
            items[fullname] = item
            gtk.idle_add(paths[path].insert, item, -1)
    