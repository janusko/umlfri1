from lib.lib import ToBool
from lib.Exceptions.UserException import *
from lib.Base import CBaseObject
import weakref

class CElementType(CBaseObject):
    '''
    Scheme for a class of elements
    '''
    
    def __init__(self, factory, id):
        '''
        create new instance of element type
        '''
        self.icon = None
        self.id = id
        self.labels = []
        self.attributes = {}
        self.connections = {}
        self.appearance = None
        self.attributeList = []
        self.generatename = True
        self.domain = None
        self.counter = 0
        self.options = {}
        self.identity = None
        if factory is None:
            self.factory = lambda:None
        else:
            self.factory = weakref.ref(factory)
    
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
    
    def SetIdentity(self, identity):
        '''
        Change element identity
        
        @param identity: Name of property acting as unique identifier of element
        @type identity: string
        '''
        self.identity = identity
    
    def GetIdentity(self):
        '''
        Determine element identity
        
        @return: Name of property acting as unique identifier of element
        @rtype: string
        '''
        return self.identity
    
    def AppendOptions(self, name, value):
        self.options[name] = value
    
    def GetOptions(self):
        return self.options
    
    def GenerateName(self):
        '''
        @return: new name for object, name
        @rtype: str
        '''
        self.counter += 1
        return self.id + str(self.counter)
        
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
    
    def AppendConnection(self, value, withobject, allowrecursive):
        '''
        add allowed connection as defined in metamodel
        '''
        self.connections[value] = (withobject, allowrecursive)

    def AddLabel(self, position, label):
        """
        Add label to element type

        @param position: initial position of label. See L{ElementLabelInfo<lib.Drawing.ElementLabelInfo>}.
        @type  position: string

        @param label: visual object representing the label
        @type  label: L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}
        """
        self.labels.append((position, label))

    def RemoveLabel(self, label):
        """
        Remove label from element

        @param label: visual object representing the label
        @type  label: L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}
        """
        for id, i in enumerate(self.labels):
            if i[1] is label:
                del self.labels[id]
                return
        else:
            raise ConnectionError("LabelNotExists")

    def GetLabels(self):
        """
        Get list of all labels on this element type

        @return: all labels
        @rtype:  iterator over (string, L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}) pairs
        """
        for label in self.labels:
            yield label
    
    def GetAppearance(self):
        '''
        @return: appearance as was defined in metamodel
        '''
        return self.appearance
                
    def GetConnections(self):
        '''
        iterator over allowed connections
        
        @return: tuple of values (withobject, allowrecursive)
        '''
        for item in self.connections.iteritems():
            yield item
    
    def GetIcon(self):
        '''
        @return: relative path to the icon of current type
        @rtype: str
        '''
        return self.icon
    
    def GetId(self):
        '''
        @return: ID or name of the element type as used in metamodel
        @rtype: str
        '''
        return self.id
    
    def GetResizable(self, context):
        '''
        @return: True if element can be resized - depends on the uppermost
        authoritative visual object.
        @rtype: bool
        '''
        return self.appearance.GetResizable(context)
    
    def Paint(self, context, canvas):
        '''
        Paint element type using context
        '''
        self.appearance.Paint(context, canvas)
    
    def SetAppearance(self, appearance):
        '''
        Set appearance as defined in metamodel
        '''
        self.appearance = appearance
    
    def SetIcon(self, pixbuf):
        '''
        set relative path to the icon
        '''
        self.icon = pixbuf
    
    def SetId(self, id):
        '''
        set identifier / name of the current element type
        '''
        self.id = id
    
    def GetSize(self, context):
        '''
        @return: size as tuple {width, height)
        '''
        return self.appearance.GetSize(context)
    
    def HasVisualAttribute(self, name):
        '''
        @note: This is fake function for interface compatibility reasons
        
        @return: True if name points to anything but "text" domain attribute
        @rtype: bool
        '''
        return self.GetDomain().GetAttribute(name)['type'] != 'text'

    def GetFactory(self):
        return self.factory()

    def GetMetamodel(self):
        return self.GetFactory().GetMetamodel()