from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Drawing.Diagram import CDiagram
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject

class IDiagram(IBase):
    __cls__ = CDiagram
    
    def GetName(self):
        return self.GetName()
    
    def SetName(self, name):
        self.SetName(name)
        IBase.adapter.plugin_change_domain_value(self, CDiagram.NAME_PROPERY)
    
    @parameter('obj', t_classobject(CElementObject))
    def HasElementObject(self, obj):
        return self.HasElementObject(obj) is not None
    
    @parameter('obj', t_classobject(CConnectionObject))
    @result(r_object)
    def GetConnection(self, obj):
        return self.GetConnection(obj)
    
    def GetPath(self):
        return self.GetPath()
    
    def GetType(self):
        return self.GetType().GetId()
    
    

