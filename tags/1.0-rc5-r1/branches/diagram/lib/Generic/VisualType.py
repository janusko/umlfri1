from DomainType import CDomainType

class CVType(CDomainType):
    
    def __init__(self, id, identity, appearance):
        
        CDomainType.__init__(self, id, identity)
        self.appearance = appearance
    
    def Paint(self, context):
        """
        Paint connection of given type on canvas
        
        @param context: context in which is connection being drawn
        @type  context: L{CDrawingContext<lib.Drawing.Context.DrawingContext.CDrawingContext>}
        """
        self.appearance.Paint(context)
    
    def SetAppearance(self, appearance):
        '''
        Set appearance as defined in metamodel
        '''
        self.appearance = appearance
        
    def HasVisualAttribute(self, name):
        '''
        @note: This is fake function for interface compatibility reasons
        
        @return: True if name points to anything but "text" domain attribute
        @rtype: bool
        '''
        return self.GetDomain().GetAttribute(name)['type'] != 'text'

