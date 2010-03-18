from common import CGuiObject, event
from lib.Depend.gtk2 import gobject
from GuiManager import CGuiManager
from lib.Base import CBaseObject


class CPluginAdapter(CBaseObject, CGuiObject):
    
    def __init__(self, app):
        CGuiObject.__init__(self, app)
        self.guiManager = CGuiManager(app)
        self.manager = None
        self.GetUID()
        
    def _generateUID(self):
        return 'adapter'
        
    def _SetPluginManager(self, pluginManager):
        self.manager = pluginManager
        
    def GetGuiManager(self):
        return self.guiManager
        
    def GetProject(self):
        return self.application.GetProject()
    
    def GetCurrentDiagram(self):
        return self.application.GetWindow('frmMain').picDrawingArea.GetDiagram()
        
        
    @event('application.bus', 'content-update')
    def gui_change_domain_value(self, widget, element, property):
        self.manager.DomainValueChanged(element, property)
    
    def plugin_change_domain_value(self, element, property):
        gobject.idle_add(self.application.GetBus().emit, 'content-update', element, property)
    
    def plugin_display_warning(self, text):
        gobject.idle_add(self.application.GetBus().emit, 'run-dialog', 'warning', text)
    
    def GetCanvas(self):
        return self.application.GetWindow('frmMain').picDrawingArea.canvas
