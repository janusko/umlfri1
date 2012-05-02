from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Gui.pluginAdapter import CPluginAdapter

class IAdapter(IBase):
    __cls__ = CPluginAdapter
    
    def GetProject(him):
        return him.GetProject()
        
    def GetCurrentDiagram(him):
        return him.GetCurrentDiagram()
    
    def SetCurrentDiagram(him, value):
        him.SelectDiagramTab(value)
    
    def AddNotification(him, event, callback):
        him.AddNotification(event, callback)

    def RemoveNotification(him, event, callback):
        him.RemoveNotification(event, callback)
        
    def Notify(him, event, *args, **kwds):
        return him.Notify(event, *args, **kwds)
    
    def GetGuiManager(him):
        return him.GetGuiManager()

    def LoadProject(him, fileName):
        him.LoadProject(fileName)
    
    @includeAddr
    def GetTransaction(him, _addr):
        return him.GetPluginManager().GetTransaction(_addr)
    
    def GetTemplates(him):
        return list(him.GetTemplateManager().GetAllTemplates())
