def CreateModifications(project):
    if not project.GetRoot().HasChild():
        return

    mmBuilder = project.CreateModification()
    emBuilder = mmBuilder.CreateElementModifications(project.GetRoot())
    emBuilder.AddDomainAttribute('Class', 'class', 'docstring',
                                 dict(
                                     name='Documentation string',
                                     type='text'))

    modification = mmBuilder.Build()
    modification.Apply()
    pass