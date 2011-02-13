from DomainObject import IDomainObject
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Domains.Object import CDomainObject
from lib.Exceptions import *
from lib.Project import CProjectNode

class IElementObject(IDomainObject):
    __cls__ = CElementObject
    
    def GetName(him):
        return him.GetName()
    
    def GetDiagrams(him):
        node = him.GetNode()
        if node is not None:
            return node.GetDiagrams()
    
    def GetConnections(him):
        return list(him.GetConnections())
        
    def GetChildren(him):
        node = him.GetNode()
        if node is not None:
            return [n.GetObject() for n in node.GetChilds()]
        
    def GetAppears(him):
        return list(him.GetAppears())
    
    
