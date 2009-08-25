from lib.Addons.Plugin.Interface.Classes.base import IBase
from common import CGuiObject, event
from lib.Depend.gtk2 import gobject

class CPluginAdapter(CGuiObject):
    
    def __init__(self, app):
        CGuiObject.__init__(self, app)
        self.manager = app.GetPluginManager()
        self.app = app
        IBase.SetAdapter(self)
        
    @event('application.bus', 'content-update')
    def gui_change_domain_value(self, widget, element, property):
        self.manager.DomainValueChanged(element, property)
    
    def plugin_change_domain_value(self, element, property):
        gobject.idle_add(self.application.GetBus().emit, 'content-update', element, property)
    
    def plugin_display_warning(self, text):
        gobject.idle_add(self.application.GetBus().emit, 'run-dialog', 'warning', text)
    
    def GetCanvas(self):
        return self.app.GetWindow('frmMain').picDrawingArea.canvas
