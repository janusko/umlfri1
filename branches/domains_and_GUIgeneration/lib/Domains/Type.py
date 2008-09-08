from Item import CDomainItem

class EDomainTypeError(Exception):
    pass

class CDomainType(object):
    
    def __init__(self, name):
        
        self.name = name
        self.imports = []
        self.items = {}
    
    def AppendItem(self, value, type, propid=None, itemtype=None, options=[]):
        '''
        Add value filed 
        '''
        
        if not type in self.imports:
            raise EDomainTypeError('Used type %s is not imported'%(type, ))
        self.items[value] = CDomainItem(type, options)

    def AppendImport(self, name):
        '''
        Add name of domain that current uses
        
        Only imported domains are allowed to be used
        
        @param name: name of imported domain
        @type name: str
        '''
        assert isinstance(name, (str, unicode))
        self.imports.append(name)
        
    def HasImportLoop(self, factory, name = None):
        '''
        Search for loops in domain import tree
        
        @return: True if name is found in 
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
                return factory.GetDomain(imported).HasImportLoop(factory, name)
        
        return False #nothing is imported
    
