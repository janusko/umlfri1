class EDomainObject(Exception): pass

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
        
        self.type = type
        self.values = {}
        for id in self.type.IterItemID():
            if self.type.IsAtomic(id):
                self.values[id] = self.type.GetDefaultValue(id)
            else:
                self.values[id] = CDomainObject(self.type.GetItem(id)['type'])
    
    def GetType(self):
        '''
        @return: logical type of current object
        @rtype: L{CDomainType<Type.CDomainType>}
        '''
        return self.type
    
    def GetValue(self, id)
        '''
        Get value of field. Type can be one of atomic types or CDomainObject
        object if type is non-atomic
        
        @retrun: value of filed defined by id
        @rtype: various
        
        @raise EDomainObject: if id is not recognized
        
        @param id: field identifier
        @type id: str
        '''
        if not id in self.values:
            raise EDomainObject('Identifier "%s" unknown'%(id, ))
        
        return self.values[id]
    
    def SetValue(self, id, value):
        '''
        Set value of field defined by id. Value type must corespond to the 
        definition.
        
        @param id: field identifier
        @type id: str
        
        @param value: value of field
        @type value: various
        
        @raise EDomainObject: if id is not recognized
        '''
        
        if not id in self.values:
            raise EDomainObject('Identifier "%s" unknown'%(id, ))
        
        
