from lib.Depend.gtk2 import gobject
from lib.Depend.gtk2 import gtk

from lib.Gui.common import CWidget, CellRendererButton, event
from lib.Drawing import CDiagram
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Exceptions import *

ID_ID, ID_NAME, ID_VALUE, ID_TEXT_VISIBLE, ID_COMBO_VISIBLE, ID_EDITABLE, ID_BUTTON_VISIBLE, ID_MODEL, ID_BUTTON_TEXT, ID_ACTION, ID_COLOR,  ID_FONT = range(12)

EDITABLE_COMBO_TYPES = ('int', 'float', 'str')

class ClwProperties(CWidget):
    name = 'lwProperties'
    widgets = ('lwProperties',)
    
    def __init__(self, app, wTree):
        
        self.element = None
        
        self.treeStore = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN, gobject.TYPE_BOOLEAN, gobject.TYPE_BOOLEAN, gobject.TYPE_BOOLEAN, gtk.TreeModel, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
        
        renderer = gtk.CellRendererText()
        self.Column1 = gtk.TreeViewColumn(_('Name'))
        self.Column1.pack_start(renderer, True)
        self.Column1.add_attribute(renderer, 'text', ID_NAME)
        self.Column1.set_resizable(True)
                 
        self.StrRenderer = gtk.CellRendererText()
        self.StrRenderer.set_property('editable', True)
        
        self.ComboRenderer = gtk.CellRendererCombo()
        self.ComboRenderer.set_property('text-column', 0)
        self.ComboRenderer.set_property('editable', ID_EDITABLE)
        self.ComboRenderer.set_property('has-entry', ID_EDITABLE)
        
        self.Column2 = gtk.TreeViewColumn(_('Value'))
        self.Column2.pack_start(self.StrRenderer, True)
        self.Column2.pack_start(self.ComboRenderer, True)
        
        self.Column2.add_attribute(self.StrRenderer, 'text', ID_VALUE)
        self.Column2.add_attribute(self.StrRenderer, 'editable', ID_EDITABLE)
        self.Column2.add_attribute(self.StrRenderer, 'visible', ID_TEXT_VISIBLE)
        
        self.Column2.add_attribute(self.ComboRenderer, 'model', ID_MODEL)
        self.Column2.add_attribute(self.ComboRenderer, 'has-entry', ID_EDITABLE)
        self.Column2.add_attribute(self.ComboRenderer, 'visible', ID_COMBO_VISIBLE)
        self.Column2.add_attribute(self.ComboRenderer, 'text', ID_VALUE)
        
        self.ButtonRenderer = CellRendererButton()
        CWidget.__init__(self, app, wTree)
        
        self.Column2.pack_start(self.ButtonRenderer, False)
        self.Column2.add_attribute(self.ButtonRenderer, 'visible', ID_BUTTON_VISIBLE)
        self.Column2.add_attribute(self.ButtonRenderer, 'text', ID_BUTTON_TEXT)
        self.Column2.add_attribute(self.ButtonRenderer, 'editable', ID_EDITABLE)
        self.Column2.add_attribute(self.ButtonRenderer, 'color', ID_COLOR)
        self.Column2.add_attribute(self.ButtonRenderer, 'font', ID_FONT)
        
        self.lwProperties.append_column(self.Column1)
        self.lwProperties.append_column(self.Column2)
        self.lwProperties.set_model(self.treeStore)
        
    
    def _FillListItem(self, object, parent, prefix, idx):
        itemrow = self.treeStore.append(parent)
        self.treeStore.set(itemrow,
            ID_ID, '[%i]' % idx,
            ID_NAME, str(idx), 
            ID_VALUE, '', #text representation of item in list
            ID_TEXT_VISIBLE, False, 
            ID_COMBO_VISIBLE, False, 
            ID_BUTTON_VISIBLE, True, 
            ID_EDITABLE, False, #Change to True if has parser
            ID_BUTTON_TEXT, 'Delete',
            ID_ACTION, 'listdel')
        self._FillBody(object, itemrow, prefix + '[%i]' % idx)
    
    def _FillBody(self, object, parent, prefix):
        
        DType = object.GetDomainType(prefix)
        
        for attrID in DType.IterAttributeIDs():
            identifier = ('.' if prefix else '') + attrID
            type = DType.GetAttribute(attrID)['type']
            name = DType.GetAttribute(attrID)['name']
            
            if DType.IsHidden(attrID) or type in ('list','text') or not DType.IsAtomic(domain = type):
                continue
            
            row = self.treeStore.append(parent)
            
            if type in EDITABLE_COMBO_TYPES and not DType.GetAttribute(attrID).has_key('enum'):
                self.treeStore.set(row, 
                    ID_ID, identifier,
                    ID_NAME, name, 
                    ID_VALUE, str(object.GetValue(prefix + identifier)), 
                    ID_TEXT_VISIBLE, True, 
                    ID_COMBO_VISIBLE, False, 
                    ID_BUTTON_VISIBLE, False, 
                    ID_EDITABLE, True)
            
            elif type in ('enum', 'bool') or (type in EDITABLE_COMBO_TYPES and DType.GetAttribute(attrID).has_key('enum')):
                model = gtk.ListStore(gobject.TYPE_STRING)
                for item in (DType.GetAttribute(attrID)['enum'] if type != 'bool' else ('True', 'False')):
                    model.set(model.append(), 0 , item)
                self.treeStore.set(row, 
                    ID_ID, identifier,
                    ID_NAME, name, 
                    ID_VALUE, str(object.GetValue(prefix + identifier)), 
                    ID_TEXT_VISIBLE, False, 
                    ID_COMBO_VISIBLE, True, 
                    ID_BUTTON_VISIBLE, False, 
                    ID_EDITABLE, type in EDITABLE_COMBO_TYPES, 
                    ID_MODEL, model,)
            
            elif type=='color':
                color = gtk.gdk.color_parse(str(object.GetValue(prefix + identifier)))
                text = '('+str(int(round(color.red / 256))) + ', '+str(int(round(color.green / 256))) + ', '+str(int(round(color.blue / 256))) +')'
                self.treeStore.set(row, 
                    ID_ID, identifier,
                    ID_NAME, name, 
                    ID_VALUE, str(object.GetValue(prefix + identifier)), #text representation of color
                    ID_TEXT_VISIBLE, False, 
                    ID_COMBO_VISIBLE, False, 
                    ID_BUTTON_VISIBLE, True, 
                    ID_EDITABLE, False, #Change to True if has parser
                    ID_BUTTON_TEXT, text,
                    ID_ACTION, 'changecolor',
                    ID_COLOR, str(object.GetValue(prefix + identifier)))
                    
            elif type=='font':
                self.treeStore.set(row, 
                    ID_ID, identifier,
                    ID_NAME, name, 
                    ID_VALUE, str(object.GetValue(prefix + identifier)), #text representation of font
                    ID_TEXT_VISIBLE, False, 
                    ID_COMBO_VISIBLE, False, 
                    ID_BUTTON_VISIBLE, True, 
                    ID_EDITABLE, False, #Change to True if has parser
                    ID_BUTTON_TEXT, str(object.GetValue(prefix + identifier)),
                    ID_ACTION, 'changefont',
                    ID_FONT, str(object.GetValue(prefix + identifier)),
                    ID_COLOR, "")
    
    def __GetElementObject(self):
        if self.element is None:
            return None
        elif isinstance(self.element, (CElementObject, CConnectionObject, CDiagram)):
            return self.element
        else:
            return self.element.GetObject()
    
    def Fill(self, Element):
        self.element = Element
            
        self.treeStore.clear()
        
        if Element is  None:
            return
        self._FillBody(self.__GetElementObject(), None, '')
    
    def Clear(self):
        self.element = None
        self.treeStore.clear()
    
    def get_key(self, path):
        model = self.lwProperties.get_model()
        path = path.split(':')
        return ''.join([ model.get(model.get_iter_from_string(':'.join(path[:i+1])), ID_ID)[0] for i in xrange(len(path)) ])
        
    @event('StrRenderer', 'editing-started')
    def on_editing_started (self, cellrenderer, editable, path):
        self.application.GetBus().emit('properties-editing-started')
    
    @event('StrRenderer', 'editing-canceled')
    def on_eiditing_canceled (self, cellrenderer):
        self.application.GetBus().emit('properties-editing-stoped')

    @event("StrRenderer", "edited")
    def on_change_text(self, cellrenderer, path, new_value):
        model = self.lwProperties.get_model()
        iter = model.get_iter_from_string(path)
        model.set(iter, ID_VALUE, new_value) 
        key = self.get_key(path)
        
        elementObject = self.__GetElementObject()
        
        try:
            elementObject.SetValue(key, new_value)
        except (DomainTypeError, ), e:
            model.set(iter, ID_VALUE, str(elementObject.GetValue(key)))
            raise ParserError(*e.params)
        self.application.GetBus().emit('content-update', self.element, key)
        self.application.GetBus().emit('properties-editing-stoped')
        
    @event("ComboRenderer", "edited")
    def on_change_combo(self, cellrenderer, path, new_value):
        model = self.lwProperties.get_model()
        iter = model.get_iter_from_string(path)
        model.set(iter, ID_VALUE, new_value)
        key = self.get_key(path)
        
        elementObject = self.__GetElementObject()
        
        try:
            elementObject.SetValue(key, new_value)
        except (DomainTypeError, ), e:
            model.set(iter, ID_VALUE, str(elementObject.GetValue(key)))
            raise ParserError(*e.params)
        self.application.GetBus().emit('content-update', self.element, key)
        
    def on_changecolor(self, key, iter):
        cdia = gtk.ColorSelectionDialog("Select color")
        colorsel = cdia.colorsel
        
        elementObject = self.__GetElementObject()
        
        if elementObject.GetValue(key) is not None:
            colorsel.set_current_color(gtk.gdk.color_parse(elementObject.GetValue(key)))
        response = cdia.run()
        
        if response == gtk.RESPONSE_OK:
            colorsel = cdia.colorsel
            color = colorsel.get_current_color()
            model = self.lwProperties.get_model()
            elementObject.SetValue(key, color.to_string())
            model.set(iter, ID_VALUE, str(elementObject.GetValue(key)))
            text = '('+str(int(round(color.red / 256))) + ', '+str(int(round(color.green / 256))) + ', '+str(int(round(color.blue / 256))) +')'
            model.set(iter, ID_BUTTON_TEXT, text)
            model.set(iter, ID_COLOR, elementObject.GetValue(key))
        cdia.destroy()

        self.application.GetBus().emit('content-update', self.element, key)
        
    def on_changefont(self, key, iter):
        fdia = gtk.FontSelectionDialog("Select font")
        
        elementObject = self.__GetElementObject()
        
        if elementObject.GetValue(key) is not None:
            fdia.set_font_name(elementObject.GetValue(key))
        
        response = fdia.run()
        
        if response == gtk.RESPONSE_OK:
            
            font_desc = fdia.get_font_name()

            
            model = self.lwProperties.get_model()
            elementObject.SetValue(key, font_desc)
            model.set(iter, ID_VALUE, str(elementObject.GetValue(key)))
            model.set(iter, ID_BUTTON_TEXT, str(elementObject.GetValue(key)))
            model.set(iter, ID_FONT, str(elementObject.GetValue(key)))
        fdia.destroy()

        self.application.GetBus().emit('content-update', self.element, key)
        
    def on_listadd(self, key, iter):
        elementObject = self.__GetElementObject()
        
        elementObject.AppendItem(key)
        self._FillListItem(elementObject, iter, key, len(elementObject.GetValue(key)) - 1)
        self.application.GetBus().emit('content-update', self.element, key)
        
    def on_listdel(self, key, iter, path):
        model = self.lwProperties.get_model()
        parent_path = path.rsplit(':', 1)[0]
        parent_iter = model.get_iter_from_string(parent_path)
        parent_key = self.get_key(parent_path)
        
        elementObject = self.__GetElementObject()
        
        if len(elementObject.GetValue(parent_key)) == 1:
            self.lwProperties.collapse_row(parent_path)
            self.on_listadd(parent_key, parent_iter)
        elementObject.RemoveItem(key)
        self.treeStore.remove(iter)
        for idx in xrange(int(path.rsplit(':', 1)[-1]), len(elementObject.GetValue(parent_key))):
            npath = parent_path + ':' + str(idx)
            niter = model.get_iter_from_string(npath)
            self.treeStore.set(niter,
                ID_ID, '[%i]' % idx,
                ID_NAME, str(idx))
        self.application.GetBus().emit('content-update', self.element, key)
    
    
    
    @event("ButtonRenderer", "click")
    def on_change_button(self, cellrenderer, path):
        model = self.lwProperties.get_model()
        iter = model.get_iter_from_string(path)
        action, = model.get(iter, ID_ACTION)
        key = self.get_key(path)
        if action == 'listadd':
            self.on_listadd(key, iter)
            
        elif action == 'listdel':
            self.on_listdel(key, iter, path)
        elif action == 'changecolor':
            self.on_changecolor(key, iter)
        elif action == 'changefont':
            self.on_changefont(key, iter)

    @event('application.bus', 'content-update-from-plugin')
    def on_content_update(self, widget, element, property):
        if self.element is not None and element is self.element:
            self.Fill(self.element)
    
    @event('application.bus', 'diagram-changed')
    @event('application.bus', 'connection-changed')
    @event('application.bus', 'element-changed')
    def ObjectChanged(self, bus, params):
        if self.element is None:
            return
        
        for obj, path in params:
            if path:
                if not isinstance(obj, (CElementObject, CConnectionObject)):
                    obj = obj.GetObject()
                if self.__GetElementObject() is obj:
                    self.Fill(self.element)
