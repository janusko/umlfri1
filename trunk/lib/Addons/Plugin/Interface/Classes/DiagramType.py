from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Diagrams.Type import CDiagramType
from lib.Elements.Type import CElementType
from lib.Connections.Type import CConnectionType

class IDiagramType(IBase):
    __cls__ = CDiagramType
    
    def GetName(him):
        return him.GetId()
    
    def GetConnections(him):
        cf = him.GetMetamodel().GetConnectionFactory()
        result = [cf.GetConnection(i) for i in him.GetConnections()]
        return result
    
    def GetElements(him):
        ef = him.GetMetamodel().GetElementFactory()
        return [ef.GetElement(i) for i in him.GetElements()]
        
