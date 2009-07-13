from GenericType import CGenericType

class CIconType(CGenericType):
    
    def __init__(self, id, icon):
        
        CGenericType.__init__(self, id)
        self.icon = icon
        
    def GetIcon(self):
        '''
        @return: icon path
        @rtype: string
        '''
        return self.icon
    
    def SetIcon(self, value):
        """
        Set icon path to new value
        
        @param value: icon path
        @type  value: string
        """
        self.icon = value
    


