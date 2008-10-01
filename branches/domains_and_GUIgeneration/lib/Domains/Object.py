from lib.Exceptions import DomainObjectError

class CDomainObject(object):
    '''
    representation of logical element attribute - its value
    '''
    
    def __init__(self, type):
        '''
        create new instance
        
        all the inner values are set to default values defined by type.
        Non-atomic inner values are set to another CDomainObject objects
        creating tree-like structure.
        
        @param type: domain type of current object - definition
        @type type: L{CDomainType<Type.CDomainType>}
        '''
        
        if isinstance(type, (str, unicode)):
            raise DomainObjectError('string cannot be used as domain reference')
        self.type = type
        self.values = {}
        for id in self.type.IterAttributesID():
            self.values[id] = self.type.GetDefaultValue(id)
    
    def GetType(self):
        '''
        @return: logical type of current object
        @rtype: L{CDomainType<Type.CDomainType>}
        '''
        return self.type
    
    def GetValue(self, id):
        '''
        Get value of field. Type can be one of atomic types or CDomainObject
        object if type is non-atomic
        
        @retrun: value of filed defined by id
        @rtype: various
        
        @raise DomainObjectError: if id is not recognized
        
        @param id: field identifier
        @type id: str
        '''
        if not id in self.values:
            raise DomainObjectError('Identifier "%s" unknown'%(id, ))
        
        return self.values[id]
    
    def SetValue(self, id, value):
        '''
        Set value of field defined by id. 
        
        domain of field must corenspond to the definition. Two possibilities
        are allowed:
            - id is defined with atomic domain. Look at 
            L{CDomainType.TransformValue<Type.CDomainType.TransformValue>}
            - id is defined as non-atomic domain. In this case, value MUST be
            instance of CDomainObject with the same domain as defined.
        
        @param id: field identifier
        @type id: str
        
        @param value: value of field
        @type value: various
        
        @raise EDomainType: if id has atomic type and value cannot be 
        transformed to this type
        
        @raise DomainObjectError: if id has non-atomic type and domain of value
        doesn't correspond to definition
        '''
        
        if not id in self.values:
            raise DomainObjectError('Identifier "%s" unknown'%(id, ))
        
        self.values[id] = self.type.TransformValue(id, value)
    
    def GetSaveInfo(self):
        '''
        @return: structured dictionary containing all the necessary data for .frip file
        @rtype: dict
        '''
        return dict([(id, self.type.PackValue(id, value)) for id, value in self.values.iteritems()])
    
    def SetSaveInfo(self, data):
        '''
        Restore all the attribute values from dictionary loaded from .frip file
        
        @param data: structured dictionary as returned from 
        L{self.GetSaveInfo<self.GetSaveInfo>}
        @type data: dict
        '''
        for key, value in data.iteritems():
            if isinstance(value, dict):
                self.GetValue(key).SetSaveInfo(value)
            elif isinstance(value, (list, str, unicode)):
                self.SetValue(key, value)
