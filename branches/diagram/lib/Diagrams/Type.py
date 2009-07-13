from lib.Generic import CIconType, CDomainType, CNameType

class CDiagramType(CIconType, CDomainType, CNameType):
    """
    Type of diagram
    """
    def __init__(self, id, icon = None, identity = None):
        """
        Initialize diagram type
        
        @param id: Name of the diagram type
        @type  id: string
        """
        
        CIconType.__init__(self, id, icon)
        CDomainType.__init__(self, id, identity)
        CNameType.__init__(self, id)
        self.elements = []
        self.connections = []
    
    def AppendElement(self, value):
        """
        Append the element type to this diagram type
        
        @param value: Element, which has to be added to the diagram type
        @type  value: L{ElementType<lib.Elements.ElementType.CElementType>}
        """
        self.elements.append( value )
        
    def AppendConnection(self, value):
        """
        Append the connection type to this diagram type
        
        @param value: Connection, which has to be added to the diagram type
        @type  value: L{ConnectionType<lib.Connections.ConnectionType.CConnectionType>}
        """
        self.connections.append( value )
        
    def GetConnections(self):
        """
        Get list of connections allowed to be added to diagram of this type
        
        @return: List of connection types
        @rtype:  iterator over L{ConnectionType<lib.Connections.ConnectionType.CConnectionType>}(s)
        """
        for connection in self.connections:
            yield connection
        
    def GetElements(self):
        """
        Get list of elements allowed to be added to diagram of this type
        
        @return: List of element types
        @rtype:  iterator over L{ElementType<lib.Elements.ElementType.CElementType>}(s)
        """
        for element in self.elements:
            yield element
    
