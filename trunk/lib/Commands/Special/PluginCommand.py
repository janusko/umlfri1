from lib.Commands.Base.Command import CCommand

class CPluginCommand(CCommand):
    def __init__(self, pluginUri, pluginName):
        CCommand.__init__(self)
        
        self.__commands = []
        self.__pluginName = pluginName
        self.__pluginUri = pluginUri
        self.__rolledBack = False
    
    def Execute(self, command):
        if self.__rolledBack:
            raise Exception("Incorrect call to execute, transaction is rolled back")
        if self.IsDone():
            raise Exception("Incorrect call to execute, transaction is committed")
        
        command.Do()
        if not command.IsError():
            self.__commands.append(command)
    
    def Rollback(self):
        if self.__rolledBack:
            raise Exception("Incorrect call to rollback, transaction is already rolled back")
        if self.IsDone():
            raise Exception("Incorrect call to rollback, transaction is committed")
        
        self.__rolledBack = True
        self._Undo()
    
    def _Do(self):
        if self.__rolledBack:
            raise Exception("Cannot do rolled back transaction")
    
    def _Redo(self):
        for cmd in self.__commands:
            cmd.Redo()
    
    def _Undo(self):
        for cmd in self.__commands:
            cmd.Undo()
    
    def GetGuiUpdates(self):
        return [upd for cmd in self.__commands for upd in cmd.GetGuiUpdates()]
    
    def __str__(self):
        if self.__pluginName is None:
            return _("Action from plugin")
        else:
            return _("Action from plugin %s") % self.__pluginName
