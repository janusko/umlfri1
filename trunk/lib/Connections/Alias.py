from lib.Exceptions.UserException import *
import weakref

class CConnectionAlias(object):
    '''
    Scheme for a class of connections
    '''
    
    def __init__(self, factory, id, aliasType):
        '''
        create new instance of connection type
        '''
        self.icon = None
        self.id = id
        self.aliasType = aliasType
        self.defaultValues = {}
        self.factory = weakref.ref(factory)
        self.options = {}
    
    def SetDefaultValue(self, path, value):
        self.defaultValues[path] = value
    
    def GetDefaultValues(self):
        return self.defaultValues.iteritems()
    
    def GetIcon(self):
        '''
        @return: relative path to the icon of current type alias
        @rtype: str
        '''
        return self.icon
    
    def GetId(self):
        '''
        @return: ID or name of the connection type alias as used in metamodel
        @rtype: str
        '''
        return self.id
    
    def GetAlias(self):
        '''
        @return: ID or name of the aliased connection type as used in metamodel
        @rtype: str
        '''
        return self.aliasType
    
    def GetAliasType(self):
        return self.factory().GetConnection(self.aliasType)
    
    def SetIcon(self, pixbuf):
        '''
        set relative path to the icon
        '''
        self.icon = pixbuf
    
    def GetMetamodel(self):
        return self.factory().GetMetamodel()
