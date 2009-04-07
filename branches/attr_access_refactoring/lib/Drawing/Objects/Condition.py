from SimpleContainer import CSimpleContainer


class CCondition(CSimpleContainer):
    params = {
        'condition': bool,
    }
    def __init__(self, condition):
        CSimpleContainer.__init__(self)
        self.condition = condition

    def ComputeSize(self, context):
        condition, = self.GetVariables(context, 'condition')
        if condition:
            return CSimpleContainer.ComputeSize(self, context)
        return (0, 0)

    def Paint(self, context):
        condition, = self.GetVariables(context, 'condition')
        if condition:
            CSimpleContainer.Paint(self, context)
