from lib.Domains.AttributeConditions import BuildParam


def CreateModifications(project):
    if not project.GetRoot().HasChild():
        return

    modificationRoot = list(project.GetRoot().GetChilds())[2]

    emBuilder = modificationRoot.CreateModification()
    emBuilder.AddDomainAttribute('Class', 'class', 'docstring',
                                 dict(
                                     name='Documentation string',
                                     type='text',
                                     hidden=False,
                                     default=None,
                                     condition=BuildParam('#self.sealed')
                                 ))
    emBuilder.AddDomainAttribute('Class', 'class', 'sealed',
                                 dict(
                                     name='Sealed',
                                     type='bool',
                                     hidden=False,
                                     default=False
                                 ))

    modification = emBuilder.Build()
    modification.Apply()

    modificationRoot = list(project.GetRoot().GetChilds())[3]
    emBuilder = modificationRoot.CreateModification()
    emBuilder.AddDomainAttribute('Class', 'class', 'final',
                                 dict(
                                     name='Final',
                                     type='bool',
                                     hidden=False,
                                     default=None
                                 ))
    emBuilder.Build().Apply()
    pass