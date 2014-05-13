from SimpleContainer import CSimpleContainer


class CCondition(CSimpleContainer):
    types = {
        'condition': bool,
    }
    def __init__(self, condition):
        CSimpleContainer.__init__(self)
        self.condition = condition
    
    def GetResizable(self, context):
        condition, = self.GetVariables(context, 'condition')
        if condition:
            return CSimpleContainer.GetResizable(self, context)
        return False, False

    def ComputeSize(self, context):
        condition, = self.GetVariables(context, 'condition')
        if condition:
            return CSimpleContainer.ComputeSize(self, context)
        return (0, 0)

    def Paint(self, context, canvas):
        condition, = self.GetVariables(context, 'condition')
        if condition:
            CSimpleContainer.Paint(self, context, canvas)
