from math import atan2
from lib.Exceptions.UserException import *
from lib.Generic import CIconType, CVisualType

class CConnectionType(CIconType, CVisualType):
    """
    Contains part of metamodel that represents connection type
    """
    def __init__(self, id, appearance, icon = None, identity = None):
        """
        Initialize connection type and fill its properties
        
        @param id: name of this connection type
        @type  id: string
        
        @param icon: path to connection icon within metamodel storage
        @type  icon: string
        
        @param identity: Name of property acting as unique identifier of connection
        @type  identity: string
        """
        CIconType.__init__(self, id, icon)
        CVisualType.__init__(self, id, identity, appearance)
        self.labels = []
    
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
    
