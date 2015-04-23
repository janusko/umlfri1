from lib.Addons.Metamodel.ModifiedMetamodel import CModifiedMetamodel
from lib.Addons.Plugin.Interface.Classes.Metamodel import IMetamodel


class IModifiedMetamodel(IMetamodel):
    __cls__ = CModifiedMetamodel