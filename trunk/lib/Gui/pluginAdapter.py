from common import CGuiObject, event
from lib.Depend.gtk2 import gobject
from GuiManager import CGuiManager
from lib.Base import CBaseObject
from lib.Drawing.Connection import CConnection
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Project import CProjectNode


class CPluginAdapter(CBaseObject, CGuiObject):
    
    def __init__(self, app):
        CGuiObject.__init__(self, app)
        self.guiManager = CGuiManager(app)
        self.manager = None
        self.GetUID()
        self._persistent = True
        self.notifications = {}
    
    def AddNotification(self, event, callback):
        self.notifications.setdefault(event, []).append(callback)
            
    def RemoveNotification(self, event, callback):
        if event in self.notifications:
            for i in self.notifications[event]:
                if i._callbackId == callback._callbackId:
                    self.notifications[event].remove(i)
                    break
        else:
            raise ValueError()
    
    def Notify(self, event, *args, **kwds):
        if event in self.notifications:
            for callback in self.notifications[event]:
                if ((hasattr(callback, 'im_func') and 
                    getattr(callback.im_func, '_synchronized', False)) or 
                    getattr(callback, '_synchronized', False)
                ):
                    gobject.idle_add(callback, *args, **kwds)
                else:
                    callback(*args, **kwds)
        
    def _generateUID(self):
        return 'adapter'
        
    def _SetPluginManager(self, pluginManager):
        self.manager = pluginManager
    
    def GetPluginManager(self):
        return self.manager
        
    def GetGuiManager(self):
        return self.guiManager
        
    def GetProject(self):
        return self.application.GetProject()
    
    def GetCurrentDiagram(self):
        if self.application.GetWindow('frmMain').nbTabs.IsStartPageActive():
            return None
        else:
            return self.application.GetWindow('frmMain').picDrawingArea.GetDiagram()
    
    def GetApplication(self):
        return self.application
        
    @event('application.bus', 'content-update')
    @event('application.bus', 'content-update-from-plugin')
    def gui_change_domain_value(self, widget, element, property):
        if isinstance(element, CProjectNode):
            element = element.GetObject()
        self.Notify('content-update', element, property)
    
    @event('application.bus', 'project-opened')
    def gui_project_opened(self, widget):
        self.Notify('project-opened')
    
    def plugin_change_domain_value(self, element, property):
        gobject.idle_add(self.application.GetBus().emit, 'content-update-from-plugin', element, property)
    
    def plugin_change_object(self, object):
        if isinstance(object, (CElement, CConnection)):
            obj = object.GetObject()
        else:
            obj = object
        
        if isinstance(obj, CElementObject):
            gobject.idle_add(self.application.GetBus().emit, 'element-created-from-plugin', obj)
        
        gobject.idle_add(self.application.GetBus().emit, 'all-content-update', object)
    
    def plugin_diagram_created(self, diagram):
        gobject.idle_add(self.application.GetBus().emit, 'diagram-created-from-plugin', diagram)
    
    def plugin_add_new_element(self, element):
        picDrawingArea = self.application.GetWindow('frmMain').picDrawingArea
        picDrawingArea.emit('add-element', element.GetObject(), element.GetDiagram(), element.GetDiagram().GetNode())
        picDrawingArea.ToPaint()
        
    def plugin_add_element(self, element):
        self.application.GetWindow('frmMain').picDrawingArea.ToPaint()
        
    def GetCanvas(self):
        return self.application.GetWindow('frmMain').picDrawingArea.canvas
    
    def LoadProject(self, fileName):
        self.application.ProjectDelete()
        self.application.ProjectInit()
        self.GetProject().LoadProject(fileName)
        gobject.idle_add(self.application.GetBus().emit, 'project-opened-from-plugin-adapter')
        
    def GetUmlfriVersion(self):
        return self.application.GetVersion()
    
    def SelectDiagramTab(self, diagram):
        if diagram is not None:
            self.application.GetWindow('frmMain').nbTabs.AddTab(diagram)
            self.application.GetWindow('frmMain').picDrawingArea.SetDiagram(diagram)
        else:
            self.application.GetWindow('frmMain').nbTabs.SetStartPageAsCurrentPage()
