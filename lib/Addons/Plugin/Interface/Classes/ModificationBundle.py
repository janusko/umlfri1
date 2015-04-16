from lib.Addons.Metamodel.Modifications.ProjectNodeModificationBundleBuilder import \
    CProjectNodeModificationBundleBuilder
from lib.Addons.Plugin.Interface.Classes.base import IBase


class IModificationBundle(IBase):

    __cls__ = CProjectNodeModificationBundleBuilder

    def ReplaceAttributeBool(him, domain, id, name, default, hidden):
        him.ReplaceDomainAttributeBool(domain, id, name, default, hidden)

    def ReplaceAttributeInt(him, domain, id, name, default, hidden, min, max):
        him.ReplaceDomainAttributeInt(domain, id, name, default, hidden, min, max)

    def ReplaceAttributeFloat(him, domain, id, name, default, hidden, min, max):
        him.ReplaceDomainAttributeFloat(domain, id, name, default, hidden, min, max)

    def ReplaceAttributeStr(him, domain, id, name, default, hidden, enumValues):
        if enumValues:
            enumValues = enumValues.split('|')
        him.ReplaceDomainAttributeStr(domain, id, name, default, hidden, enumValues)

    def ReplaceAttributeText(him, domain, id, name, default, hidden):
        him.ReplaceDomainAttributeText(domain, id, name, default, hidden)

    def RemoveAttribute(him, domain, attributeID):
        him.RemoveDomainAttribute(domain, attributeID)