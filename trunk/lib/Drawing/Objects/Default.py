from SimpleContainer import CSimpleContainer
from lib.datatypes import CColor, CFont

class CDefault(CSimpleContainer):
    types = {
        'textcolor': CColor,
        'textfont': CFont
    }
    
    def __init__(self, textcolor = None, textfont = None):
        CSimpleContainer.__init__(self)
        self.textcolor = textcolor
        self.textfont = textfont
    
    def __PushToContext(self, context):
        textcolor, textfont = self.GetVariables(context, 'textcolor', 'textfont')
        
        context.Push()
        
        if textcolor is not None:
            context.SetDefault('textcolor', textcolor)
        
        if textfont is not None:
            context.SetDefault('textfont', textfont)
    
    def ComputeSize(self, context):
        self.__PushToContext(context)
        
        ret = CSimpleContainer.ComputeSize(self, context)
        
        context.Pop()
        
        return ret
    
    def Paint(self, context, canvas):
        self.__PushToContext(context)
        
        CSimpleContainer.Paint(self, context, canvas)
        
        context.Pop()
