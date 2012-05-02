from lib.Base.BaseObject import CBaseObject
from lib.Commands.Special import CPluginCommand
from lib.Exceptions import *
#~ import lib.debug

class CTransaction(CBaseObject):
    _persistent = True
    
    def __init__(self, manager, addr):
        self.buf = []
        self.state = 'unspecified'
        self.__manager = manager
        self.__addr = addr
        self.__command = None
    
    def __CreateCommand(self):
        name = None
        uri = None
        if self.__addr is not None:
            plug = self.__manager.GetPlugin(self.__addr)
            
            if plug is not None:
                name = plug.GetAddon().GetName()
                uri = plug.GetAddon().GetDefaultUri()
        
        return CPluginCommand(uri, name)
    
    def __UndoCommand(self, command):
        command.Rollback()
    
    def __DoCommand(self, command):
        self.__manager.GetPluginAdapter().GetCommands().Execute(command)
    
    def Action(self, callable, obj, fname, args, kwds, other, addr):
        if self.state == 'autocommit':
            command = self.__CreateCommand()
        elif self.state == 'transaction':
            command = self.__command
        else:
            raise TransactionModeUnspecifiedError()
        callable(obj, fname, (command, ) + args, kwds, other, addr)
        
        if self.state == 'autocommit':
            self.__DoCommand(command)
    
    def GetState(self):
        return self.state
    
    def StartAutocommit(self):
        if self.state == 'transaction':
            raise TransactionPendingError()
        else:
            self.state = 'autocommit'
    
    def EndAutocommit(self):
        if self.state != 'autocommit':
            raise InvalidTransactionMode()
        else:
            self.state = 'unspecified'
    
    def BeginTransaction(self):
        if self.state in ('autocommit', 'unspecified'):
            self.state = 'transaction'
            self.__command = self.__CreateCommand()
        else:
            raise TransactionPendingError()
    
    def CommitTransaction(self):
        if self.state == 'transaction':
            self.state = 'unspecified'
            self.__DoCommand(self.__command)
            self.__command = None
        else:
            raise OutOfTransactionError()
    
    def RollbackTransaction(self):
        if self.state == 'transaction':
            self.buf = []
            self.state = 'unspecified'
            self.__UndoCommand(self.__command)
            self.__command = None
        else:
            raise OutOfTransactionError()
            
