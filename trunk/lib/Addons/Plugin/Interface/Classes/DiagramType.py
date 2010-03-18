from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Diagrams.Type import CDiagramType
from lib.Elements.Type import CElementType
from lib.Connections.Type import CConnectionType

class IDiagramType(IBase):
    __cls__ = CDiagramType
    
    @result(r_str)
    def GetName(him):
        return him.GetId()
    
    @result(r_objectlist)
    def GetConnections(him):
        cf = him.GetMetamodel().GetConnectionFactory()
        result = [cf.GetConnection(i) for i in him.GetConnections()]
        print result
        return result
    
    @result(r_objectlist)
    def GetElements(him):
        ef = him.GetMetamodel().GetElementFactory()
        return [ef.GetElement(i) for i in him.GetElements()]
        
