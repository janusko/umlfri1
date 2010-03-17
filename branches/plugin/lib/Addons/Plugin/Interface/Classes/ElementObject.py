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
    
    @result(r_objectlist)
    def GetDiagrams(him):
        node = him.GetNode()
        if node is not None:
            return node.GetDiagrams()
    
    @result(r_objectlist)
    def GetConnections(him):
        return list(him.GetConnections())
        
    @result(r_objectlist)
    def GetChilds(him):
        node = him.GetNode()
        if node is not None:
            return [n.GetObject() for n in node.GetChilds()]
        
    
    #destructive
    
    #~ @factory
    #~ @parameter('type', t_elementType)
    #~ def Create(type):
        #~ return CElementObject(type)
    
    #~ @parameter('child', t_classobject(CElementObject))
    #~ def AddChild(him, child):
        #~ node = him.GetNode()
        #~ if node is not None:
            #~ node.AddChild(CProjectNode(object = child))
    
    #~ @parameter('con', t_classobject(CConnectionObject))
    #~ def AddConnection(him, con):
        #~ return him.AddConnection(con)
    
    #~ @parameter('con', t_classobject(CConnectionObject))
    #~ def Disconnect(him, con):
        #~ him.Disconnect(con)
    
