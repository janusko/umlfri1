from lib.Commands.Project.ApplyModifiedMetamodel import CApplyModifiedMetamodelCommand
from lib.Domains.AttributeConditions import BuildParam


def CreateModifications(project):
    if not project.GetRoot().HasChild():
        return

    modificationRoot = list(project.GetRoot().GetChilds())[2]

    emBuilder = modificationRoot.CreateModification()
    bundleBuilder = emBuilder.CreateBundle("bundle 1")
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

    metamodel1 = emBuilder.BuildMetamodel()

    modificationRoot = list(project.GetRoot().GetChilds())[3]
    emBuilder = modificationRoot.CreateModification()
    bundleBuilder = emBuilder.CreateBundle("bundle 2")
    bundleBuilder.AddDomainAttribute('Class', 'class', 'final',
                                 dict(
                                     name='Final',
                                     type='bool',
                                     hidden=False,
                                     default=None
                                 ))
    metamodel2 = emBuilder.BuildMetamodel()

    metamodels = [metamodel1, metamodel2]
    for m in metamodels:
        yield CApplyModifiedMetamodelCommand(m.GetRootNode(), m)