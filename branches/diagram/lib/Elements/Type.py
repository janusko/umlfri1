from lib.lib import ToBool
from lib.Exceptions.UserException import *
from lib.Generic import CIconType, CVisualType, CNameType

class CElementType(CIconType, CVisualType, CNameType):
    '''
    Scheme for a class of elements
    '''
    
    def __init__(self, id, appearance, icon = None, identity = None):
        '''
        create new instance of element type
        '''
        
        CIconType.__init__(self, id, icon)
        CVisualType.__init__(self, id, identity, appearance)
        CNameType.__init__(self, id)
        self.attributes = {}
        self.connections = {}
        self.attributeList = []
        self.options = {}
    
    def AppendOptions(self, name, value):
        self.options[name] = value
    
    def GetOptions(self):
        return self.options
    
    def AppendConnection(self, value, withobject, allowrecursive):
        '''
        add allowed connection as defined in metamodel
        '''
        self.connections[value] = (withobject, allowrecursive)
    
    def GetConnections(self):
        '''
        iterator over allowed connections
        
        @return: tuple of values (withobject, allowrecursive)
        '''
        for item in self.connections.iteritems():
            yield item
    
    def GetResizable(self):
        '''
        @return: True if element can be resized - depends on the uppermost
        authoritative visual object.
        @rtype: bool
        '''
        return self.appearance.GetResizable()
    
    def GetSize(self, context):
        '''
        @return: size as tuple {width, height)
        '''
        return self.appearance.GetSize(context)
    
