from lib.Addons.Metamodel.Modifications.ModificationBundleBuilder import CMetamodelModificationBundleBuidler
from lib.Commands.Project.ApplyModificationBundles import CApplyModificationBundles
from lib.Domains.AttributeConditions import BuildParam


def CreateModifications(project):
    if not project.GetRoot().HasChild():
        return

    modificationRoot = list(project.GetRoot().GetChilds())[2]

    mbBuilder = CMetamodelModificationBundleBuidler()
    bundleBuilder = mbBuilder.CreateBundle("bundle 1")
    bundleBuilder.AddDomainAttribute('Class', 'class', 'docstring',
                                 dict(
                                     name='Documentation string',
                                     type='text',
                                     hidden=False,
                                     default=None,
                                     condition=BuildParam('#self.sealed')
                                 ))
    bundleBuilder.AddDomainAttribute('Class', 'class', 'sealed',
                                 dict(
                                     name='Sealed',
                                     type='bool',
                                     hidden=False,
                                     default=False
                                 ))

    modification1 = (modificationRoot, mbBuilder.BuildBundles())

    modificationRoot = list(project.GetRoot().GetChilds())[3]
    mbBuilder = CMetamodelModificationBundleBuidler()
    bundleBuilder = mbBuilder.CreateBundle("bundle 2")
    bundleBuilder.AddDomainAttribute('Class', 'class', 'final',
                                 dict(
                                     name='Final',
                                     type='bool',
                                     hidden=False,
                                     default=None
                                 ))
    modification2 = (modificationRoot, mbBuilder.BuildBundles())

    modifications = [modification1, modification2]
    for (root, bundles) in modifications:
        yield CApplyModificationBundles(root, bundles)