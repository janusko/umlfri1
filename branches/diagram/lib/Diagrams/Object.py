from lib.Exceptions import *
import weakref

class CDiagramObject(object):
    '''
    Represents logic of diagram
    '''
    
    
    
    def __init__(self, type):
        '''
        @param type: Diagram type instance
        @type type: L{CDiagramType<Type.CDiagramType>}
        '''
        self.type = type
