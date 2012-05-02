from GenericType import CGenericType

class CNameType(CGenericType):
    
    def __init__(self, id):
        
        CGenericType.__init__(self, id)
        self.counter = 0
        
    def GenerateName(self):
        '''
        @return: new name for object, name
        @rtype: str
        '''
        self.counter += 1
        return self.id + ' ' + str(self.counter)
        
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
        assert type(value) in (int, long)
        self.counter = value
    

