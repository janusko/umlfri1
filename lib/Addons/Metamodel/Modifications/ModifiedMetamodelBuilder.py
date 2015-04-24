from itertools import chain
from lib.Addons.Metamodel.Modifications.DomainFactory import CDomainTypeFactory
from lib.Addons.Metamodel.Modifications.DomainModificationMerger import CDomainModificationMerger
from lib.Addons.Metamodel.ModifiedMetamodel import CModifiedMetamodel
from lib.Domains.ModifiedFactory import CModifiedDomainFactory
from lib.Domains.ModifiedType import CModifiedDomainType
from lib.Elements import CElementAlias
from lib.Elements.ModifiedType import CModifiedElementType


class CModifiedMetamodelBuilder(object):

    __domainModificationMerger = CDomainModificationMerger()
    __domainTypeFactory = CDomainTypeFactory()

    def BuildMetamodel(self, elementNode, modificationBundles, parentMetamodel = None):
        if parentMetamodel is None:
            parentMetamodel = elementNode.GetObject().GetType().GetMetamodel()

        domainModifications = self.__GetDomainModifications(modificationBundles)
        if parentMetamodel.IsModified():
            inheritedDomainModifications = self.__GetDomainModifications(parentMetamodel.GetModificationBundles())

            domainModifications = self.__domainModificationMerger.MergeModifications(inheritedDomainModifications, domainModifications)

        modifiedMetamodel = CModifiedMetamodel(parentMetamodel, elementNode, modificationBundles)

        modifiedElementFactory = modifiedMetamodel.GetElementFactory()
        modifiedDomainFactory = modifiedMetamodel.GetDomainFactory()

        # algorithm overview:
        # two parts:
        # - create modified domains
        # - create modified element types

        # - encapsulate element types from parent metamodel with new element type
        # - if there are modifications for given element type, stop and process them:
        #   - create modified domain factory
        #   - create modified domain types

        # creating modified domains:
        # - take domain from parent metamodel
        # - create modified domain type
        #   - either take modifications defined for this domain, or create empty list
        # - collect modified domains into modified domain factory

        # Even domains, which are not modified, have to be replaced with CModifiedDomainType,
        # because we need to have access to modified metamodel even from elements that are not modified
        # (e.g. create new operation inside class, i.e. inside 'class' CDomainObject create new CDomainObject
        # for 'class.operations' domain)

        for domain in parentMetamodel.GetDomainFactory().IterTypes():
            name = domain.GetName()

            if domainModifications.has_key(name):
                modifications = domainModifications[name]
            else:
                modifications = []

            domain = CModifiedDomainType(domain, modifiedDomainFactory, modifications)
            modifiedDomainFactory.AddDomain(domain)

        for name, modifications in domainModifications.iteritems():
            if modifiedDomainFactory.HasDomain(name):
                continue

            domain = self.__domainTypeFactory.CreateDomainFromModifications(name, modifiedDomainFactory, modifications)
            modifiedDomainFactory.AddDomain(domain)

        # creating modified element types:
        # - take element type from parent metamodel
        # - retrieve modified domain for this element from modified domain factory
        # - create element type with this domain
        # - collect modified element types into modified element factory

        # Similar as for domains: need to create CModifiedElementType for all element types
        # (e.g. create modified element 'class' as child of unmodified element 'package')

        for elementType in parentMetamodel.GetElementFactory().IterTypes():
            if isinstance(elementType, CElementAlias):
                continue

            modifiedElementType = CModifiedElementType(elementType, modifiedElementFactory)
            modifiedElementFactory.AddType(modifiedElementType)

            domain = modifiedDomainFactory.GetDomain(elementType.GetDomain().GetName())
            modifiedElementType.SetDomain(domain)

        return modifiedMetamodel

    def __GetDomainModifications(self, modificationBundles):
        modifications = None
        for bundle in modificationBundles:
            if not modifications:
                modifications = bundle.GetDomainModifications()
            else:
                modifications = self.__domainModificationMerger.MergeModifications(modifications, bundle.GetDomainModifications())
        return modifications