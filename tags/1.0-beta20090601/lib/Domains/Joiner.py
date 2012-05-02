import re
from Object import CDomainObject

class CDomainJoiner(object):
    '''
    Joiner supporting joins according to self.joiner
    @ivar joiner: string used to replace domain representation
    '''
    def __init__(self, joiner):
        '''
        @param joiner: string used to replace domain representation
        @type joiner: str  
        '''
        self.joiner = joiner;
        
    def __str__(self):
        result = ['<CDomainJoiner']
        result.append(' joiner ="')
        result.append(self.joiner)
        result.append('">')
        return ''.join(result)
    
    def replace(self, obj):
        def tmp(param):
            return '%s'%(obj.GetValue(param.group(1)))
        return tmp
    
    def CreateString(self, obj):
        '''
        Creates string from domain representation according to joiner representation
        @param obj: DomainObject
        @type obj: L{CDomainObject<CDomainObject>}
        
        @rtype: str
        '''
        reVAL = re.compile('#([a-z]+)')
        return reVAL.sub(self.replace(obj), self.joiner)