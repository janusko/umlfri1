from lib.Base import CBaseObject


class CAttributeEvaluationContext(CBaseObject):

    def __init__(self, object):
        self.object = object

    def GetDomainObject(self):
        return self.object
