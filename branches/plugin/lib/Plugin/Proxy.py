import thread, time, sys, socket, re
from interface import interface
from lib.Depend.gtk2 import gtk
from ComSpec import *
from lib.Exceptions import *

class CProxy(object):
    
    def __init__(self, manager):
        self.manager = manager
        self.guimanager = manager.GetGuiManager()
    
    def Error(self, addr):
        print 'ERROR', addr
    
    def Stopped(self, id):
        print 'Stopped', id
        return True
    
    def Command(self, command, params, data, addr):
        print 'Command', command, params, data
        
        if command['version'] == '1.0':
            try:
                com = command['command'].lower()
                
                if com == 'gui':
                    self._gui(command['type'].lower(), params, addr)
                    
                else:
                    self.manager.Send(addr, RESP_UNKONWN_COMMAND, command = com)
            
            except (ParamValueError, ), e:
                self.manager.Send(addr, RESP_INVALID_PARAMETER, **dict((i, params[i])for i in e))
            except (ParamMissingError, ), e:
                self.manager.Send(addr, RESP_MISSING_PARAMETER, param = e.args[0])
        
        else:
            self.manager.Send(addr, RESP_UNSUPPORTED_VERSION, version = command['version'])
    
    def _gui(self, ctype, params, addr):
        try:
            if ctype == 'add':
                self._addgui(params, addr)
            
            elif ctype == 'sensitive':
                self.guimanager.SetSensitive(params['path'], True)
                self.manager.Send(addr, RESP_GUI_SENSITIVE, path = params['path'])
            
            elif ctype == 'insensitive':
                self.guimanager.SetSensitive(params['path'], False)
                self.manager.Send(addr, RESP_GUI_INSENSITIVE, path = params['path'])
                
            else:
                self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = com, type = ctype)
            
        except (KeyError, ), e:
            raise ParamMissingError(e.message)
        
    
    def _addgui(self, params, addr):
        mtype = params['type'] 
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
            item.connect('activate', self._guiactivated, addr, params['path'] + '/' + params['name'])
            item.show()
            self.guimanager.AddMenuItem(item, params['name'], params['path'])
            self.manager.Send(addr, RESP_GUI_ADDED, type = mtype, fullname = params['path'] + '/' + params['name'])
        
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
            item.connect('clicked', self._guiactivated, addr, params['path'] + '/' + params['name'])
            item.show()
            self.guimanager.AddButton(item, params['name'], params['path'])
            self.manager.Send(addr, RESP_GUI_ADDED, type = mtype, fullname = params['path'] + '/' + params['name'])
        
        elif mtype == 'submenu':
            self.guimanager.AddSubmenu(params['path'])
            self.manager.Send(addr, RESP_GUI_ADDED, type = mtype, fullname = params['path'])
        
        else:
            raise ParamValueError(params['type'])
    
    def _guiactivated(self, item, path, addr):
        print 'GuiActivated', path, addr
        self.manager.Send(addr, RESP_GUI_ACTIVATED, path = path)
