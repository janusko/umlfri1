from lib.Domains.AttributeConditions import BuildParam


def CreateModifications(project):
    if not project.GetRoot().HasChild():
        return

    modificationRoot = list(project.GetRoot().GetChilds())[2]

    mmBuilder = modificationRoot.CreateModification()
    emBuilder = mmBuilder.CreateElementModifications(modificationRoot)
    emBuilder.AddDomainAttribute('Class', 'class', 'docstring',
                                 dict(
                                     name='Documentation string',
                                     type='text',
                                     hidden=False,
                                     default=None,
                                     condition=BuildParam('#self.stereotype == "interface"')
                                 ))

    modification = mmBuilder.Build()
    modification.Apply()
    pass