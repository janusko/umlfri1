from lib.Base import CBaseObject
from lib.Drawing.Context.DomainAttributeEvalWrapper import CDomainAttributeEvalWrapper


class CDomainAttributesEvalWrapper(CBaseObject):

    def __init__(self, type):
        self._type = type

    def __convert(self, attribute):
        return CDomainAttributeEvalWrapper(attribute)

    def __getattr__(self, name):
        raise TypeError("No attributes on CDomainAttributesEvalWrapper")

    def __getitem__(self, name):
        if self._type.HasAttribute(name):
            return self.__convert(self._type.GetAttribute(name))
        else:
            return None

    def __iter__(self):
        for id in self._type.IterAttributeIDs():
            yield id, self.__convert(self._type.GetAttribute(id))

    def __len__(self):
        return self._type.GetAttributesCount()
