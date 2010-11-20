from math import atan2
from lib.Exceptions.UserException import *
from lib.Base import CBaseObject

import weakref

class CConnectionType(CBaseObject):
    """
    Contains part of metamodel that represents connection type
    """
    def __init__(self, factory, id, appearance, icon = None, domain = None, identity = None):
        """
        Initialize connection type and fill its properties
        
        @param id: name of this connection type
        @type  id: string
        
        @param icon: path to connection icon within metamodel storage
        @type  icon: string
        
        @param identity: Name of property acting as unique identifier of connection
        @type  identity: string
        """
        self.id = id
        self.icon = icon
        self.labels = []
        self.domain = domain
        self.identity = identity
        self.appearance = appearance
        self.factory = weakref.ref(factory)
    
    def GetDomain(self):
        '''
        @return: current domain type
        @rtype: L{CDomainType<lib.Domain.Type.CDomainType>}
        '''
        return self.domain
    
    def SetDomain(self, domain):
        '''
        Set current domain type
        
        @param domain: new domain type
        @type domain: L{CDomainType<lib.Domain.Type.CDomainType>}
        '''
        self.domain = domain
    
    def GetConnectionIdentity(self):
        '''
        Determine connection identity
        
        @return: Name of property acting as unique identifier of connection
        @rtype: L{CDomainType<lib.Domain.Type.CDomainType>}
        '''
        return self.identity
    
    def SetConnectionIdentity(self, identity):
        '''
        Change identity of connection
        
        @param identity: Name of property acting as unique identifier of connection
        @type identity: string
        '''
        self.identity = identity
    
    def SetIcon(self, value):
        """
        Set icon path to new value
        
        @param value: icon path
        @type  value: string
        """
        self.icon = value
    
    def AddLabel(self, position, label):
        """
        Add label to connection type
        
        @param position: initial position of label.
            (one of source, center, destination)
        @type  position: string
        
        @param label: visual object representing the label
        @type  label: L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}
        """
        self.labels.append((position,label))
    
    def RemoveLabel(self, label):
        """
        Remove label from connection
        
        @param label: visual object representing the label
        @type  label: L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}
        """
        for id, i in enumerate(self.labels):
            if i[1] is label:
                del self.labels[id]
                return
        else:
            raise ConnectionError("LabelNotExists")
    
    def GetIcon(self):
        """
        Get the icon of this connection
        
        @return: icon path within metamodel storage
        @rtype:  string
        """
        return self.icon
    
    def GetId(self):
        """
        Return name (Id) of this connection type
        
        @return: name of connection
        @rtype:  string
        """
        return self.id

    def Paint(self, context):
        """
        Paint connection of given type on canvas
        
        @param context: context in which is connection being drawn
        @type  context: L{CDrawingContext<lib.Drawing.Context.DrawingContext.CDrawingContext>}
        """
        self.appearance.Paint(context)
    
    def GetLabels(self):
        """
        Get list of all labels on this connection type
        
        @return: all labels
        @rtype:  iterator over (string, L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>}) pairs
        """
        for label in self.labels:
            yield label
    
    def GetLabel(self, idx):
        """
        Get label by its index
        
        @param idx: index
        @type  idx: integer
        
        @return: all labels
        @rtype:  (string, L{CVisualObject<lib.Drawing.Objects.VisualObject.CVisualObject>})
        """
        return self.labels[idx]
    
    def HasVisualAttribute(self, name):
        '''
        @note: This is fake function for interface compatibility reasons
        
        @return: True if name points to anything but "text" domain attribute
        @rtype: bool
        '''
        return self.GetDomain().GetAttribute(name)['type'] != 'text'
    
    def GetMetamodel(self):
        return self.factory().GetMetamodel()
