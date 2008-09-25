from lib.lib import ToBool
from lib.Exceptions.UserException import *

class CElementType(object):
    '''
    Scheme for a class of elements
    '''
    
    def __init__(self, id):
        self.icon = None
        self.id = id
        self.attributes = {}
        self.connections = {}
        self.appearance = None
        self.visAttrs = {}
        self.attributeList = []
        self.generatename = True
        self.domain = None
    
    def SetDomain(self, domain):
        self.domain = domain
    
    def GetDomain(self):
        return self.domain
    
    def AppendConnection(self, value, withobject, allowrecursive):
        self.connections[value] = (withobject, allowrecursive)
    
    def GetAppearance(self):
        return self.appearance
                
    def GetConnections(self):
        for item in self.connections.iteritems():
            yield item
    
    def GetIcon(self):
        return self.icon
    
    def GetId(self):
        return self.id
    
    def GetResizable(self):
        return self.appearance.GetResizable()
    
    def GetAttribute(self, key):
        return self.attributes[key]
    
    def GetGenerateName(self):
        return self.generatename
        
    def SetGenerateName(self, generate):
        self.generatename = generate
        
    def Paint(self, context):
        self.appearance.Paint(context)
    
    def SetAppearance(self, appearance):
        self.appearance = appearance
    
    def SetIcon(self, pixbuf):
        self.icon = pixbuf
    
    def SetId(self, id):
        self.id = id
    
    def HasVisualAttribute(self, id):
        return id in self.visAttrs.itervalues()
    
    def GetVisAttr(self, id):
        if id in self.visAttrs:
            return self.visAttrs[id]
        else:
            raise ElementAttributeError('VisAttrDontExists')
    
    def GetSize(self, context):
        return self.appearance.GetSize(context)
