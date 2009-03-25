import thread, time, sys, socket, re
from interface import interface
from lib.Depend.gtk2 import gtk
from Communication.ComSpec import *
from lib.Exceptions import *

class CProxy(object):
    
    def __init__(self, manager, app):
        self.manager = manager
        self.app = app
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
                
                elif com == 'metamodel':
                    self._metamodel(command['type'].lower(), params, addr)
                    
                else:
                    self.manager.Send(addr, RESP_UNKONWN_COMMAND, command = com)
            
            except (ParamValueError, ), e:
                self.manager.Send(addr, RESP_INVALID_PARAMETER, params = [i for i in e])
            except (ParamMissingError, ), e:
                self.manager.Send(addr, RESP_MISSING_PARAMETER, param = e[0])
        
        else:
            self.manager.Send(addr, RESP_UNSUPPORTED_VERSION, version = command['version'])
    
    def _metamodel(self, com, params, addr):
        try:
            ctype = com.split('.', 1)
            assert (len(ctype) == 2 and ctype[0] in ('list', 'detail') and 
                ctype[1] in ('metamodel', 'element', 'diagram', 'connection', 'domain'))
            
            if self.app.GetProject() is not None:
                metamodel = self.app.GetProject().GetMetamodel()
            else:
                self.manager.Send(addr, RESP_PROJECT_NOT_LOADED)
                return
            
            
            if ctype[0] == 'list':
                assert ctype[1] != 'metamodel'
                if ctype[1] == 'diagram':
                    result = list(metamodel.GetDiagrams())
                elif ctype[1] == 'element':
                    result = [e.GetId() for e in metamodel.GetElementFactory().IterTypes()]
                elif ctype[1] == 'connection':
                    result = [c.GetId() for c in metamodel.GetConnectionFactory().IterTypes()]
                elif ctype[1] == 'domain':
                    result = [d.GetName() for d in metamodel.GetDomainFactory().IterTypes()]
                self.manager.Send(addr, RESP_METAMODEL_DESCRIPTION, type = com, result = result)
            
            if ctype[0] == 'detail':
                if ctype[1] == 'metamodel':
                    result = {'uri': metamodel.GetUri(), 'version': metamodel.GetVersion()}
                    name = 'metamodel'
                else:
                    if 'name' in params:
                        name = params['name']
                    else:
                        raise ParamMissingError('name')
                    if ctype[1] == 'diagram':
                        diagram = metamodel.GetDiagramFactory().GetDiagram(name)
                        result = {'connection': list(diagram.GetConnections()),
                                  'element': list( diagram.GetElements())}
                    if ctype[1] == 'element':
                        element = metamodel.GetElementFactory().GetElement(name)
                        result = {'connection': list(element.GetConnections()),
                                  'domain':     element.GetDomain().GetName(),
                                  'identity':   element.GetIdentity(),
                                  'options':    element.GetOptions(),
                                  'resizable':  element.GetResizable()}
                    if ctype[1] == 'connection':
                        connection = metamodel.GetConnectionFactory().GetConnection(name)
                        result = {'domain':   connection.GetDomain().GetName(),
                                  'identity': connection.GetConnectionIdentity()}
                    if ctype[1] == 'domain':
                        domain = metamodel.GetDomainFactory().GetDomain(name)
                        result = {'attributes': [dict(id = attr, **domain.GetAttribute(attr)) for attr in domain.IterAttributeIDs()],
                                  'parsers':  list(domain.IterParsers()),}
                self.manager.Send(addr, RESP_METAMODEL_DESCRIPTION, type = com, result = result, name = name)
        
        except (AssertionError, ), e:
            self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'metamodel', type = com)
        
        except (FactoryError, ), e:
            raise ParamValueError('name')
    
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
                self.manager.Send(addr, RESP_INVALID_COMMAND_TYPE, command = 'gui', type = ctype)
            
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
            raise ParamValueError('type')
    
    def _guiactivated(self, item, path, addr):
        print 'GuiActivated', path, addr
        self.manager.Send(addr, RESP_GUI_ACTIVATED, path = path)
