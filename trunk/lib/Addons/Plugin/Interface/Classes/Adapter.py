from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Gui.pluginAdapter import CPluginAdapter

class IAdapter(IBase):
    __cls__ = CPluginAdapter
    
    @result(r_object)
    def GetProject(him):
        return him.GetProject()
        
    @result(r_object)
    def GetCurrentDiagram(him):
        return him.GetCurrentDiagram()
    
    @result(r_object)
    def GetMainMenu(him):
        return him.GetMainMenu()
        
    @result(r_object)
    def GetTabMenu(him):
        return him.GetTabMenu()
        
    @result(r_object)
    def GetTreeMenu(him):
        return him.GetTreeMenu()
    
    @result(r_object)
    def GetDrawMenu(him):
        return him.GetDrawMenu()
    
    @result(r_object)
    def GetButtonBar(him):
        return him.GetButtonBar()

