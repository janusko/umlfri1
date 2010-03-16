import weakref

class CDiagramType(object):
    """
    Type of diagram
    """
    def __init__(self, factory, id):
        """
        Initialize diagram type
        
        @param id: Name of the diagram type
        @type  id: string
        """
        self.icon = None
        self.id = id
        self.elements = []
        self.connections = []
        self.swimlines = False
        self.lifelines = False
        self.domain = None
        self.counter = 0
        self.factory = weakref.ref(factory)
    
    def GetMetamodel(self):
        return self.factory().GetMetamodel()
    
    def SetDomain(self, domain):
        '''
        @param domain: domain type that holds info about data
        @type domain: L{CDomainType<lib.Domains.Type.CDomainType>}
        '''
        self.domain = domain
    
    def GetDomain(self):
        '''
        @return: current domain type
        @rtype: L{CDomainType<lib.Domains.Type.CDomainType>}
        '''
        return self.domain
        
    def GetIdentity(self):
        '''
        Determine element identity
        
        @return: Name of property acting as unique identifier of element
        @rtype: string
        '''
        return self.identity
    
    def SetIdentity(self, identity):
        '''
        Change element identity
        
        @param identity: Name of property acting as unique identifier of element
        @type identity: string
        '''
        self.identity = identity
    
    def GenerateName(self):
        '''
        @return: new name for object, name
        @rtype: str
        '''
        self.counter += 1
        return self.id + ' ' + str(self.counter)
        
    def GetCounter(self):
        '''
        @return: current value of counter
        @rtype: int
        '''
        return self.counter
    
    def SetCounter(self, value):
        '''
        set new value to counter
        
        @param value: new value of counter
        @type value: int
        '''
        assert type(value) in (int, long)
        self.counter = value
    
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
    
    def GetIcon(self):
        """
        Return icon of this diagram type
        
        @return: path to the icon within storage
        @rtype:  string
        """
        return self.icon
    
    def GetId(self):
        """
        Return name of this diagram type
        
        @return: diagram type name
        @rtype:  string
        """
        return self.id
        
    def SetSpecial(self, swimlines, lifelines):
        """
        Set values of diagram special properties
        
        @param swimlines: if True, swimlines will be enabled on this diagram type
        @type  swimlines: boolean
        
        @param lifelines: if True, lifelines will be enabled on this diagram type
        @type  lifelines: boolean
        """
        self.swimlines = swimlines
        self.lifelines = lifelines
        
    def GetSwimlinesEnabled(self):
        """
        Determine, if swimlines are enabled on this diagram type
        
        @return: True, if swimlines are enabled
        @rtype:  boolean
        """
        return self.swimlines
        
    def GetLifelinesEnabled(self):
        """
        Determine, if lifelines are enabled on this diagram type
        
        @return: True, if lifelines are enabled
        @rtype:  boolean
        """
        return self.lifelines
    
    def SetIcon(self, path):
        """
        Set the icon for this diagram type
        
        @param path: Path to diagram icon, relative to storage root
        @type  path: string
        """
        self.icon = path
    
    def SetId(self, id):
        """
        Set name of this diagram type
        """
        self.id = id
