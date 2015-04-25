from ..Base.Command import CCommand, CommandNotDone
from lib.Addons.Metamodel.Modifications.DomainModificationMerger import CDomainModificationMerger, \
    AttributeModificationReplaceDeleteMergeStrategy
from lib.Domains.ModifiedFactory import CModifiedDomainFactory
from lib.Domains.ModifiedType import CModifiedDomainType
from lib.Domains.TypeSetter import CDomainTypeSetter


class CModifyProjectDomainCommand(CCommand):

    __domainModificationMerger = CDomainModificationMerger(
        replaceDeleteMergeStrategy=AttributeModificationReplaceDeleteMergeStrategy.CancelEachOtherOut)
    __domainTypeSetter = CDomainTypeSetter()

    def __init__(self, project, modifications):
        CCommand.__init__(self)

        self.__domainobject = project.GetDomainObject()
        self.__modifications = modifications
        self.__newType = None
        self.__oldType = None

    def _Do(self):
        # retrieve underlying type from CRuntimeDomainType
        self.__oldType = self.__domainobject.GetType().GetParentType()

        modifications = self.__modifications
        parentType = self.__oldType

        if isinstance(self.__oldType, CModifiedDomainType):
            modifications =  self.__domainModificationMerger.MergeAttributeModifications(self.__oldType.GetModifications(),
                modifications)
            parentType = self.__oldType.GetParentType()

        factory = CModifiedDomainFactory(parentType.GetFactory())

        self.__newType = CModifiedDomainType(parentType, factory, modifications)
        factory.AddDomain(self.__newType)

        self._Redo()

    def _Redo(self):
        self.__domainTypeSetter.ApplyType(self.__domainobject, self.__newType)

    def _Undo(self):
        self.__domainTypeSetter.ApplyType(self.__domainobject, self.__oldType)

    def GetGuiUpdates(self):
        return []

    def __str__(self):
        return _('Modify project domain')