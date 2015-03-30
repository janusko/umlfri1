from lib.Base import CBaseObject
from lib.Exceptions import CreateElementError


class CElementTypeValidator(CBaseObject):

    def CanCreateElementAsChild(self, type, parent):
        if type not in set(parent.GetMetamodel().GetElementFactory().IterTypes()):
            raise CreateElementError(
                "Cannot create element object - type with name '%s' is not available for use at given level of project" % type.GetId())
