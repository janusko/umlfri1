class CDomainItem(object):
    '''
    definition of one attribute a domain is made of
    '''
    
    def __init__(self, name, type, options):
        '''
        create new instance
        
        @param id: 
        '''
        self.name = name
        self.type = type
        self.options = options
    
    def GetName(self):
        return self.name
    
    def GetType(self):
        return self.type
    
    def GetOptions(self):
        return self.options