from lib.Plugin.Interface.Classes.base import IBase
from common import CGuiObject, event
from lib.Depend.gtk2 import gobject

class CPluginAdapter(CGuiObject):
    
    def __init__(self, app):
        CGuiObject.__init__(self, app)
        self.manager = app.GetPluginManager()
        IBase.SetAdapter(self)
        
    @event('application.bus', 'content-update')
    def gui_change_domain_value(self, widget, element, property):
        self.manager.DomainValueChanged(element, property)
    
    def plugin_change_domain_value(self, element, property):
        self.application.GetBus().emit('content-update', element, property)
        #~ self.frmMain.on_nbProperties_content_update(self, element, property)
        #~ self.frmMain.nbProperties.lwProperties.
