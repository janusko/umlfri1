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
