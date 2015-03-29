from lib.Exceptions.UserException import *
import weakref
from lib.Base import CBaseObject

class CElementAlias(CBaseObject):
    '''
    Scheme for a class of elements
    '''
    
    def __init__(self, factory, id, aliasType):
        '''
        create new instance of element type
        '''
        self.icon = None
        self.id = id
        self.aliasType = aliasType
        self.defaultValues = {}
        self.counter = 0
        self.factory = weakref.ref(factory)
        self.options = {}
    
    def SetDefaultValue(self, path, value):
        self.defaultValues[path] = value
    
    def GetDefaultValues(self):
        return self.defaultValues.iteritems()
    
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
        self.counter = value
    
    def GetIcon(self):
        '''
        @return: relative path to the icon of current type alias
        @rtype: str
        '''
        return self.icon
    
    def GetId(self):
        '''
        @return: ID or name of the element type alias as used in metamodel
        @rtype: str
        '''
        return self.id
    
    def GetAlias(self):
        '''
        @return: ID or name of the aliased element type as used in metamodel
        @rtype: str
        '''
        return self.aliasType
    
    def GetAliasType(self):
        return self.factory().GetElement(self.aliasType)
    
    def SetIcon(self, pixbuf):
        '''
        set relative path to the icon
        '''
        self.icon = pixbuf

    def GetFactory(self):
        return self.factory()

    def GetMetamodel(self):
        return self.GetFactory().GetMetamodel()
