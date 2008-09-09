from Item import CDomainItem

class EDomainType(Exception):
    pass

class CDomainType(object):
    
    ATOMIC = 'int', 'float', 'str', 'bool', 'enum', 'list'
    
    def __init__(self, name):
        
        self.name = name
        self.imports = []
        self.items = {}
    
    def AppendItem(self, options, id, name, type, itemtype=None):
        '''
        Add value filed to the domain
        
        @param options: list of values that enum type can hold, unused otherwise
        @type options: list
        
        @param id: identifier of item.
        @type id: str
        
        @param name: Name of item. Displayed to user
        @type name: str
        
        @param type: id of domain. Must be atomic domain or one of imported
        @type type: str
        
        @param itemtype: used if type is list. defines type of one item in list
        @type itemtype: str
        
        @raise EDomainType: 
            - if type is not atomic or one of imported domains
            - if type is "enum" and options is an empty list
        '''
        
        if not type in self.ATOMIC or not type in self.imports:
            raise EDomainType('Used type %s is not imported'%(type, ))
        
        if type == 'enum' and len(options) == 0:
            raise EDomainType('Used item %s is of type enum,'
                ' but has no valid values.'%(id, ))
        
        self.items[id] = {\
            'name': name,             
            'type':type, 
            'options': options,
            'itemtype': itemtype}

    def AppendImport(self, id):
        '''
        Add name of domain that current uses
        
        Only imported domains are allowed to be used
        
        @param id: identifier of imported domain
        @type name: str
        '''
        assert isinstance(name, (str, unicode))
        self.imports.append(name)
        
    def HasImportLoop(self, factory, id = None):
        '''
        Search for loops in domain import tree
        
        @return: True if id is found in 
        @rtype: bool
        
        @param factory: domain factory that already loaded all the domains
        @type factory: L{CDomainFactory<Factory.CDomainFactory>}
        
        @param name: name to search for. if None, current name is used
        @type name: str
        '''
        
        name = name or self.name # if None, use current name
        
        for imported in self.imports:
            if name == imported: 
                return True
            else:
                if factory.GetDomain(imported).HasImportLoop(factory, name):
                    return True
        return False
    
    def GetItem(self, id):
        '''
        get item information as an dictionary
        
        keys of the dictionary: 'name', 'type', 'options', 'itemtype'
        
        @param id: identifier of item
        @type id: str
        
        @return: information about item
        @rtype dict
        '''
        
        return self.items[id]
    
    def IterItemID(self):
        '''
        Iterator over ID of items
        
        @rtype: str
        '''
        for id in self.items.iterkeys():
            yield id
    
    def GetName(self):
        '''
        @return name of current domain
        @rtype: str
        '''
        return self.name
    
    def GetImports(self):
        '''
        @return: list of imported domains
        @rtype: list
        '''
        return self.imports
    
    def GetDefaultValue(self, id):
        '''
        @return: default value of item defined by id
        @rtype: various
        
        @raise EDomainType: 
            - when id is not valid item identifier
            - when type of item is not atomic
        
        @param id: item identifier
        @type id: str
        '''
        if not id in self.items:
            raise EDomainType('Unknown identifier %s'%(id, ))
        
        if not self.IsAtomic(id):
            raise EDomainType('Domain type "%s" is not atomic'\
                %(self.items[id]['type'], ))
        
        type = self.items[id]['type']
        if type == 'int': 
            return 0
        elif type == 'float':
            return 0.0
        elif type == 'bool':
            return False
        elif type == 'str':
            return ''
        elif type == 'list':
            return []
        elif type == 'enum':
            return self.items[id]['options'][0]
        else:
            raise EDomainType('Domain type "%s" is not atomic'\
                %(self.items[id]['type'], ))
    
    def IsAtomic(self, id):
        '''
        @return: True if item defined by id is of an atomic domain
        @rtype: bool
        
        @param id: identifier of item
        @type id: str
        
        @raise EDomainType: if id is not valid item identifier
        '''
        if not id in self.items:
            raise EDomainType('Unknown identifier %s'%(id, ))
        
        return self.items[id]['type'] in self.ATOMIC
    
    def CheckValueType(self, id, value):
        '''
        @return: True if value is of the compatible type by the definition
        @rtype: bool
        
        @param id: identifier of the item
        @type id: str
        
        @param value: value to be checked
        @type value: atomic domain
        
        @raise EDomainType: 
            - if id is not recoginzed
            - if type of item defined by id is not atomic
        '''
        
        if not id in self.items:
            raise EDomainType('Unknown identifier %s'%(id, ))
        
        if not self.IsAtomic(id):
            raise EDomainType('Item %s is of the type %s, which is not atomic'\
                %(id, self.items[id]['type']))
        
        type = self.items[id]['type']
        if type == 'int':
            if 
