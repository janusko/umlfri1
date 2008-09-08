from Item import CDomainItem
from lib.consts import ATOMIC_DOMAINS

class EDomainType(Exception):
    pass

class CDomainType(object):
    
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
        
        @raise EDomainType: if type is not atomic or one of imported domains
        '''
        
        if not type in ATOMIC_DOMAINS or not type in self.imports:
            raise EDomainType('Used type %s is not imported'%(type, ))
        self.items[id] = CDomainItem(name, type, options)

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
                return factory.GetDomain(imported).HasImportLoop(factory, name)
        
        return False #nothing is imported
    
