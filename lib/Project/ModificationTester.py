from lib.Addons.Metamodel.Modifications.ModificationBundleBuilder import CMetamodelModificationBundleBuidler
from lib.Commands.Project.ApplyModificationBundles import CApplyModificationBundlesCommand
from lib.Commands.Project.RemoveModificationBundles import CRemoveModificationBundlesCommand
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

    bundles1 = mbBuilder.BuildBundles()
    modification1 = (modificationRoot, bundles1)

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
    bundleBuilder.AddDomainAttribute('Class', 'class', 'metaclass',
                                 dict(
                                     name='Metaclass',
                                     type='enum',
                                     hidden=False,
                                     default=None,
                                     enum=['object', 'type', 'interface', 'Enum']
                                 ))
    bundleBuilder.AddDomainAttribute('Class', 'class', 'numbers',
                                 dict(
                                     name='Numbers',
                                     type='int',
                                     hidden=False,
                                     default=5,
                                     enum=[1, 2, 4, 5, 10]
                                 ))
    bundleBuilder.AddDomainAttribute('Class', 'class', 'coefficients',
                                 dict(
                                     name='Coefficients',
                                     type='float',
                                     hidden=False,
                                     default=1.2,
                                     enum=[0.8, 1.2, 2.2, 4.0, 15.44]
                                 ))
    bundles2 = mbBuilder.BuildBundles()
    modification2 = (modificationRoot, bundles2)

    modifications = [modification1, modification2]
    for (root, bundles) in modifications:
        yield CApplyModificationBundlesCommand(root, bundles)
    # yield CApplyModificationBundlesCommand(modificationRoot, merge_dicts(*[bundles for root, bundles in modifications]))
    # yield CRemoveModificationBundlesCommand(modificationRoot, bundles2)

