from ..Base.Command import CCommand, CommandNotDone

class CSetProjectPropertyValuesCommand(CCommand):
    def __init__(self, project, newValues):
        CCommand.__init__(self)

        self.__project = project
        self.__newValues = newValues
        self.__oldValues = None

    def _Do(self):
        if not self.__newValues:
            raise CommandNotDone
        self.__oldValues = dict((name, self.__project.GetDomainObject().GetValue(name)) for name in self.__newValues)

        self._Redo()

    def _Redo(self):
        for name, value in self.__newValues.iteritems():
            self.__project.GetDomainObject().SetValue(name, value)

    def _Undo(self):
        for name, value in self.__oldValues.iteritems():
            self.__project.GetDomainObject().SetValue(name, value)

    def __str__(self):
        if len(self.__newValues) == 1:
            return _("Changed property %s of the project")%(self.__oldValues.keys()[0])
        else:
            return _("Changed properties of the project")
