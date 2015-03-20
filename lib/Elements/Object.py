from lib.Exceptions.UserException import *
import weakref
from lib.Domains import CDomainObject
from Alias import CElementAlias
from lib.consts import DEFAULT_IDENTITY
from lib.Base import CBaseObject
from lib.Connections.Object import CConnectionObject

class CElementObject(CBaseObject):
    """
    Object that represents logical element and its properties
    """
    def __init__(self, type):
        """
        Initialize element object and set it into default state
        
        @param type: Type of the new element
        @type  type: L{CElementType<Type.CElementType>} or L{CElementType<Type.CElementAlias>}
        """
        self.revision = 0
        if isinstance(type, CElementAlias):
            self.type = type.GetAliasType()
        else:
            self.type = type
        self.domainobject = CDomainObject(self.type.GetDomain())
        self.connections = []
        self.node = lambda: None
        self.appears = []
        if self.type.GetIdentity() is None or self.domainobject.GetType().HasAttribute(self.type.GetIdentity()):
            self.domainobject.SetValue(self.type.GetIdentity() or DEFAULT_IDENTITY, type.GenerateName())
        if isinstance(type, CElementAlias):
            for path, value in type.GetDefaultValues():
                self.domainobject.SetValue(path, value)

    def Clone(self):
        """
        Make a copy of element object.

        @return: Element object
        @rtype: L{CElementObject}
        """
        clone = CElementObject(self.type)
        clone.node = self.node
        clone.domainobject.CopyFrom(self.domainobject)
        return clone

    def GetRevision(self):
        """
        Get revision of this object. Revision is incremented after each
        object state chage
        
        @return: Object revision
        @rtype:  integer
        """
        return self.revision
    
    def AddRevision(self):
        """
        Increase revision on external change (Like movement in project tree)
        """
        
        self.revision += 1
    
    def GetAppears(self):
        """
        Get list of object appearances on diagrams
        
        @return: list of diagrams
        @rtype:  iterator over L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        """
        for i in self.appears:
            yield i()

    def AddAppears(self, diagram):
        """
        Add element appearance
        
        @param diagram: Diagram on which element appears
        @type  diagram: L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        """
        self.appears.append(weakref.ref(diagram))

    def RemoveAppears(self, diagram):
        """
        Remove element appearance
        
        @param diagram: Diagram on which element was appearing
        @type  diagram: L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        
        @raise ValueError: if given diagram is not found
        """
        for id, value in enumerate(self.appears):
            if value() is diagram:
                del self.appears[id]
    
    def GetNode(self):
        """
        Get the project node which is associated with this element object
        
        @return: project node of this element
        @rtype:  L{CProjectNode<lib.Project.Node.CProjectNode>}
        """
        return self.node()
        
    def AddConnection(self, connection):
        """
        Add the connection object connected to this element object
        
        @param connection: connected connection
        @type  connection: L{CConnectionObject<lib.Connections.Object.CConnectionObject>}
        """
        self.revision += 1
        if connection not in self.connections:
            self.connections.append(connection)
        else:
            pass
            
    def GetConnections(self):
        """
        Get list of connections connected to this object
        
        @return: List of connected connections
        @rtype:  iterator over L{CConnectionObject<lib.Connections.Object.CConnectionObject>}(s)
        """
        for c in self.connections:
            yield c
        
    def GetType(self):
        return self.type

    def SetType(self, type):
        self.type = type

    def GetSize(self, context):
        return self.type.GetSize(context)
    
    def GetDomainName(self, key=''):
        return self.domainobject.GetDomainName(key)
    
    def GetDomainType(self, key=''):
        return self.domainobject.GetType(key)
    
    def GetDomainObject(self):
        return self.domainobject
    
    def GetValue(self, key):
        return self.domainobject.GetValue(key)
    
    def SetValue(self, key, value):
        self.domainobject.SetValue(key, value)
        self.revision += 1
        
    def GetSaveInfo(self):
        return self.domainobject.GetSaveInfo()
    
    def SetSaveInfo(self, value):
        return self.domainobject.SetSaveInfo(value)
        
    def GetName(self):
        return self.domainobject.GetValue(self.type.GetIdentity() or DEFAULT_IDENTITY)
    
    def HasVisualAttribute(self, key):
        return self.domainobject.HasVisualAttribute(key)

    def Paint(self, context, canvas):
        self.type.Paint(context, canvas)

    def Disconnect(self, connection):
        connection.Disconnect()
        
    def RemoveConnection(self, connection):
        self.revision += 1
        if connection in self.connections:
            self.connections.remove(connection)
        else:
            raise ConnectionError("ConnectionNotFound")
    
    def AppendItem(self, key, value = None):
        self.domainobject.AppendItem(key, value)
        self.revision += 1
    
    def RemoveItem(self, key):
        self.domainobject.RemoveItem(key)
        self.revision += 1
    
    def Assign(self, cprojNode):
        self.node = weakref.ref(cprojNode)
